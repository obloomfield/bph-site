# Roughly speaking, this module is most important for implementing "global
# variables" that are available in every template with the Django feature of
# "context processors". But it also does some stuff with caching computed
# properties of teams (the caching is only within a single request (?)). See
# https://docs.djangoproject.com/en/3.1/ref/templates/api/#using-requestcontext
import datetime
import inspect
import types

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from puzzles import hunt_config
from puzzles.hunt_config import (
    HOURS_PER_HINT,
    HUNT_START_TIME,
    HUNT_END_TIME,
    HUNT_CLOSE_TIME,
    HUNT_SOLUTION_TIME,
    MAJOR_CASE_SLUGS,
)
from puzzles import models
from puzzles.shortcuts import get_shortcuts


def context_middleware(get_response):
    def middleware(request):
        time = timezone.localtime()
        request.context = Context(request)
        time_after = timezone.localtime()
        # print("context_middleware: ", time_after - time)
        return get_response(request)

    return middleware


# A context processor takes a request and returns a dictionary of (key: value)s
# to merge into the request's context.


def context_processor(request):
    def thunk(name):
        return lambda: getattr(request.context, name)

    return {name: thunk(name) for name in request.context._cached_names}


# Construct a get/set property from a name and a function to compute a value.
# Doing this with name="foo" causes accesses to self.foo to call fn and cache
# the result.


def wrap_cacheable(name, fn):
    def fget(self):
        if not hasattr(self, "_cache"):
            self._cache = {}
        if name not in self._cache:
            self._cache[name] = fn(self)
        return self._cache[name]

    def fset(self, value):
        if not hasattr(self, "_cache"):
            self._cache = {}
        self._cache[name] = value

    return property(fget, fset)


# Decorator for a class, like the `Context` class below but also the `Team`
# model, that replaces all non-special methods that take no arguments other
# than `self` with a get/set property as constructed above, and also gather
# their names into the property `_cached_names`.


def context_cache(cls):
    cached_names = []
    for c in (BaseContext, cls):
        for name, fn in c.__dict__.items():
            if (
                not name.startswith("__")
                and isinstance(fn, types.FunctionType)
                and inspect.getfullargspec(fn).args == ["self"]
            ):
                setattr(cls, name, wrap_cacheable(name, fn))
                cached_names.append(name)
    cls._cached_names = tuple(cached_names)
    return cls


# This object is a request-scoped cache containing data calculated for the
# current request. As a motivating example: showing current DEEP in the top
# bar and rendering the puzzles page both need the list of puzzles the current
# team has solved. This object ensures it only needs to be computed once,
# without explicitly having to pass it around from one place to the other.


# There are currently two types of contexts: request Contexts (below) and Team
# models (in models.py). Simple properties that are generally useful to either
# can go in BaseContext. The fact that Teams are contexts enables the above
# caching benefits when calculating things like a team's solves, unlocked
# puzzles, or remaining hints -- whether you're looking at your own logged-in
# team or another team's details page.
class BaseContext:
    def now(self):
        return timezone.localtime()

    def start_time(self):
        return (
            HUNT_START_TIME - self.team.start_offset if self.team else HUNT_START_TIME
        )

    def time_since_start(self):
        return self.now - self.start_time

    def end_time(self):
        return HUNT_END_TIME

    def close_time(self):
        return HUNT_CLOSE_TIME

    def solution_time(self):
        return HUNT_SOLUTION_TIME

    # XXX do NOT name this the same as a field on the actual Team model or
    # you'll silently be unable to update that field because you'll be writing
    # to this instead of the actual model field!
    def hunt_is_prereleased(self):
        return not not self.team and self.team.is_prerelease_testsolver

    def hunt_has_started(self):
        return self.hunt_is_prereleased or self.now >= self.start_time

    def hunt_has_almost_started(self):
        return self.start_time - self.now < datetime.timedelta(hours=1)

    def hunt_is_over(self):
        return self.now >= self.end_time

    def hunt_is_closed(self):
        return self.now >= self.close_time

    def hunt_solutions_open(self):
        return self.now >= self.solution_time

    def num_metas(self):
        return len(MAJOR_CASE_SLUGS)


# Also include the constants from hunt_config.
for key, value in hunt_config.__dict__.items():
    if key.isupper() and key not in (
        "HUNT_START_TIME",
        "HUNT_END_TIME",
        "HUNT_CLOSE_TIME",
        "HUNT_SOLUTION_TIME",
    ):
        (lambda v: setattr(BaseContext, key.lower(), lambda self: v))(value)

# Also include select constants from settings.
for key in ("RECAPTCHA_SITEKEY", "GA_CODE", "DOMAIN"):
    (lambda v: setattr(BaseContext, key.lower(), lambda self: v))(
        getattr(settings, key)
    )


# The properties of a request Context are accessible both from views and from
# templates. If you're adding something with complicated logic, prefer to put
# most of it in a model method and just leave a stub call here.
@context_cache
class Context:
    def __init__(self, request):
        self.request = request

    def request_user(self):
        user = self.request.user
        return user

    def is_admin(self):
        # print("checking if admin:", self.request_user.is_staff)
        return self.request_user.is_staff

    def is_superuser(self):
        return self.request_user.is_superuser

    def is_prerelease_testsolver(self):
        return self.team.is_prerelease_testsolver if self.team else False

    def team(self):
        return getattr(self.request_user, "team", None)

    def shortcuts(self):
        return tuple(get_shortcuts(self))

    def num_hints_remaining(self):
        return self.team.num_hints_remaining if self.team else 0

    def num_free_answers_remaining(self):
        return self.team.num_free_answers_remaining if self.team else 0

    def hours_per_hint(self):
        return HOURS_PER_HINT

    def unlocks(self):
        return (
            models.Team.puzzles_by_case()
            if self.hunt_is_closed
            else models.Team.unlocks_by_case(team=self.team)
        )

    def case_unlocks(self):
        if self.hunt_is_closed:
            return models.Team.case_puzzles()

        if not self.team:
            return {}
        case_unlocks = self.team.case_unlocks
        models.Team.compute_unlocks(case_unlocks, self)
        return case_unlocks

    def major_case_unlocks(self):
        if self.hunt_is_closed:
            return {
                major_case.slug: major_case
                for major_case in models.MajorCase.objects.all()
            }

        if not self.team:
            return {}

        return self.team.major_case_unlocks

    def major_case_puzzles(self):
        if not self.team:
            return {}

        return self.team.major_case_puzzles

    #
    # def completed_hunt(self):
    #     return (self.team.runaround_solve_time is not None or self.team.all_metas_solve_time is not None) if self.team else False

    def all_puzzles(self):
        return tuple(
            models.Puzzle.objects.select_related("round").order_by(
                "round__order", "order"
            )
        )

    def unclaimed_hints(self):
        return models.Hint.objects.filter(
            status=models.Hint.NO_RESPONSE, claimer=""
        ).count()

    def visible_errata(self):
        return models.Erratum.get_visible_errata(self)

    def errata_page_visible(self):
        return self.is_superuser or any(
            erratum.updates_text for erratum in self.visible_errata
        )

    def puzzle(self):
        return None  # set by validate_puzzle

    def puzzle_unlock_time(self):
        return self.unlocks[self.puzzle]

    def time_since_unlock(self):
        return self.now - self.unlocks[self.puzzle]

    def hours_since_unlock(self):
        return self.time_since_unlock.total_seconds() // 3600

    def in_person(self):
        return self.team and self.team.in_person

    def test(self, n):
        return n * 3

    def puzzle_answer(self):
        return self.team and self.puzzle and self.team.puzzle_answer(self.puzzle)

    def guesses_remaining(self):
        return self.team and self.puzzle and self.team.guesses_remaining(self.puzzle)

    def puzzle_submissions(self):
        return self.team and self.puzzle and self.team.puzzle_submissions(self.puzzle)

    def round(self):
        return self.puzzle.round if self.puzzle else None

    # custom context definitions:

    def events_live(self):  # returns true if the user has access to events
        for puzzle in self.unlocks:
            if puzzle.round.slug == "events":
                return True
        return False

    # BPH 2024 context
    def solves(self):
        return self.team.solves if self.team else {}

    def solves_by_case(self):
        return self.team.solves_by_case if self.team else {}

    def minor_case_solves(self):
        if self.hunt_is_closed:
            return models.AnswerSubmission.all_solved_minor_cases()

        return self.team.minor_case_solves if self.team else {}

    def major_case_solves(self):
        return self.team.major_case_solves if self.team else {}

    def current_incoming_event(self):
        return models.MinorCaseIncomingEvent.get_current_incoming_event(self)

    def minor_case_active(self):
        return self.team.db_minor_case_active if self.team else {}

    def minor_case_completed(self):
        if self.hunt_is_closed:
            return models.MinorCaseCompleted.all_completed_cases()

        return self.team.db_minor_case_completed if self.team else {}

    def completed_events(self):
        return (
            models.EventCompletion.get_completed_events(self.team) if self.team else {}
        )

    def storyline_unlocks(self):
        if not self.team:
            return {}

        return models.StorylineUnlock.get_and_compute_unlocks(self.team)

    # The purpose of this logic is to keep archive links current. For example,
    # https://2019.galacticpuzzlehunt.com/archive is a page that exists but only
    # links to the 2017, 2018, and 2019 GPHs. We're not going to keep updating
    # that page for all future GPHs. Instead, we'd like to link to
    # https://galacticpuzzlehunt.com/archive, which we've set up to redirect to
    # the most recent GPH, so it'll show all GPHs run so far. If you don't have
    # an archive, you don't have to bother with this.
    def archive_link(self):
        return reverse("archive") if settings.DEBUG else "https://FIXME/archive"
