from datetime import datetime
import traceback
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from puzzles import models

from puzzles.api.api_guards import require_admin, require_auth
from puzzles.api.form_serializers import (
    TeamUpdateSerializer,
    UserRegistrationSerializer,
)

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from puzzles.signals import send_notification

from .serializers import *

from django.db import DataError


@api_view(["POST"])
def login_action(request: Request) -> Response:
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        Token.objects.get_or_create(user=user)
        login(request._request, user)
        team = Team.objects.get(user=user)
        return Response(TeamSerializer(team).data)
    else:
        return Response({"status": "failure"}, status=401)


@api_view(["POST"])
def logout_action(request: Request) -> Response:
    logout(request._request)

    return Response({"status": "success"})


@api_view(["POST"])
def register_action(request):

    context = request._request.context
    if context.hunt_has_started and not context.is_admin and not context.hunt_is_over:
        return Response(
            {"error": "Registration has closed. Please contact an admin."},
            status=400,
        )

    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = User.objects.create_user(
                serializer.validated_data.get("team_id"),
                password=serializer.validated_data.get("password"),
                first_name=serializer.validated_data.get("team_name"),
            )
            Token.objects.get_or_create(user=user)

            team = Team.objects.create(
                user=user,
                team_name=serializer.validated_data.get("team_name"),
                in_person=serializer.validated_data.get("in_person", False),
                brown_team=(
                    serializer.validated_data.get("num_brown_members") is not None
                    and serializer.validated_data.get("num_brown_members") > 0
                ),
                num_brown_members=serializer.validated_data.get("num_brown_members", 0),
                classroom_need=serializer.validated_data.get("classroom_need", False),
                where_to_find=serializer.validated_data.get("where_to_find", ""),
                phone_number=serializer.validated_data.get("phone_number", ""),
                color_choice=serializer.validated_data.get("color_choice", ""),
                emoji_choice=serializer.validated_data.get("emoji_choice", ""),
            )

            for team_member in serializer.validated_data.get("members"):
                TeamMember.objects.create(
                    team=team,
                    name=team_member.get("name"),
                    email=team_member.get("email"),
                )

            # Log in the newly registered user
            login(request._request, user)

            # Return the serialized user data
            return Response(TeamSerializer(team).data)
        # duplicate key
        except IntegrityError as e:
            return Response(
                {"error": "Username and/or team name have already been taken."},
                status=400,
            )
        except DataError as e:
            # print type of exception
            print(type(e))
            return Response(
                {
                    "error": "Your input is either too long or too short. Please make sure all required fields are filled, and of reasonable size.",
                    "error_dump": str(e),
                },
                status=400,
            )
        # input too long, etc.
        except Exception as e:
            # print type of exception
            return Response(
                {
                    "error": "An unknown error has occured. Please make sure all required fields are filled, and of reasonable size.",
                    "error_dump": str(e),
                },
                status=400,
            )
    else:
        # Return errors if registration fails
        return Response(serializer.errors, status=400)


@api_view(["POST"])
def update_team(request: Request) -> Response:
    serializer = TeamUpdateSerializer(data=request.data)

    if serializer.is_valid():

        team = Team.objects.get(user=request.user)

        team.in_person = serializer.validated_data.get("in_person", team.in_person)
        team.num_brown_members = serializer.validated_data.get(
            "num_brown_members", team.num_brown_members
        )

        team.phone_number = serializer.validated_data.get(
            "phone_number", team.phone_number
        )
        team.classroom_need = serializer.validated_data.get(
            "classroom_need", team.classroom_need
        )
        team.where_to_find = serializer.validated_data.get(
            "where_to_find", team.where_to_find
        )
        team.color_choice = serializer.validated_data.get(
            "color_choice", team.color_choice
        )
        team.emoji_choice = serializer.validated_data.get(
            "emoji_choice", team.emoji_choice
        )
        team.save()

        TeamMember.objects.filter(team=team).delete()
        for team_member in serializer.validated_data.get("members"):
            TeamMember.objects.create(
                team=team,
                name=team_member.get("name"),
                email=team_member.get("email"),
            )

        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)


@api_view(["POST"])
def move_minor_case(request: Request, round_id):
    "move minor case state"
    # print("attempted to move minor case")
    try:
        # print("team", request._request.context.team)
        # print("round_id", round_id)
        incoming_case = MinorCaseActive.objects.get(
            team=request._request.context.team, minor_case_round__id=round_id
        )
        # print(incoming_case)
        # for case in incoming_case:
        #     print(case.minor_case_round.id)
    except MinorCaseActive.DoesNotExist:
        return Response({"error": "MinorCaseIncoming not found"}, status=404)

    try:
        active_case = models.MinorCaseCompleted.objects.create(
            team=incoming_case.team,
            minor_case_round=incoming_case.minor_case_round,
            completed_datetime=incoming_case.active_datetime,
        )
        active_case.save()
    except:
        # Extract the error message from the exception
        return Response({"error": "MinorCase already completed"}, status=400)

    return Response({"success": "Move operation successful"}, status=200)


@require_admin
@api_view(["POST"])
def create_vote_event(request: Request) -> Response:
    serializer = VoteEventSerializer(data=request.data)
    team = request._request.context.team

    if serializer.is_valid():
        vote_event = MinorCaseVoteEvent.objects.create(
            timestamp=datetime.now(),
            team=team,
            selected_case=serializer.validated_data.get("selected_case"),
            incoming_event=serializer.validated_data.get("incoming_event"),
        )
        vote_event.save()

        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)


def handle_answer(
    answer: str | None, request_context, django_context, puzzle_slug: str, voucher=False
) -> Response:
    print(
        f"submitting for puzzle: {puzzle_slug} with answer: {answer} for team: {django_context.team}"
    )

    if not django_context.hunt_has_started and not django_context.is_admin:
        return Response({"error": "Hunt is not active"}, status=403)

    puzzle = Puzzle.objects.get(slug=puzzle_slug)
    unlock = PuzzleUnlock.objects.filter(team=django_context.team, puzzle=puzzle)

    if not unlock and not django_context.is_admin and not django_context.hunt_is_closed:
        return Response({"error": "Puzzle not unlocked"}, status=403)

    if request_context.team:
        guesses_left = request_context.team.guesses_remaining(puzzle)
        if guesses_left <= 0 and not voucher:
            return Response({"error": "No guesses remaining"}, status=400)

    sanitized_answer = "".join(
        [char for char in puzzle.answer if char.isalpha()]
    ).upper()
    semicleaned_guess = PuzzleMessage.semiclean_guess(answer)
    puzzle_messages = [
        message
        for message in puzzle.puzzlemessage_set.all()
        if semicleaned_guess == message.semicleaned_guess
    ]

    correct = Puzzle.normalize_answer(answer) == sanitized_answer

    if correct:
        answer = puzzle.answer  # for consistent styling on the UI

    if request_context.team:
        try:
            submission = AnswerSubmission.objects.create(
                team=django_context.team,
                puzzle=puzzle,
                submitted_answer=answer,
                is_correct=correct,
                used_free_answer=voucher,
            )
            submission.save()
        except Exception as e:
            if not puzzle_messages:
                return Response(
                    {"error": "Answer submission failed", "error_body": str(e)},
                    status=500,
                )

    # if this submission solves the minor case:
    if correct and request_context.team:
        print(f"Correct answer! ({sanitized_answer})")
        send_notification.send(
            None,
            notification_type="solve",
            data={"name": puzzle.name},
            team=django_context.team.id,
        )

        if not request_context.hunt_is_over:
            django_context.team.last_solve_time = request_context.now
            django_context.team.save()

        if puzzle.is_meta:
            print("Solved the minor case!")
            minor_case = puzzle.round
            completed = MinorCaseCompleted.objects.create(
                team=django_context.team,
                minor_case_round=minor_case,
                completed_datetime=request_context.now,
            )
            completed.save()

        elif puzzle.is_major_meta:
            print("Solved the major case!")
            major_case = MajorCase.objects.get(slug=puzzle.slug)
            completed = models.MajorCaseCompleted.objects.create(
                team=django_context.team,
                major_case=major_case,
                completed_datetime=request_context.now,
            )

    return Response(
        {
            "status": "correct" if correct else "incorrect",
            "guess": answer,
            "guesses_left": guesses_left if request_context.team else "∞",
            "messages": PuzzleMessageSerializer(puzzle_messages, many=True).data,
        },
        status=200,
    )


@api_view(["POST"])
def submit_answer(request: Request, puzzle_slug: str) -> Response:
    try:
        django_context = request._request.context
        request_context = request.context
        # answer is a query parameter:
        answer = request.query_params.get("answer")
        return handle_answer(answer, request_context, django_context, puzzle_slug)

    except Puzzle.DoesNotExist:
        return Response({"error": "Puzzle not found"}, status=404)


TESTSOLVE_TEAM = "shhh2"


@api_view(["POST"])
def unlock_case(request: Request, round_slug: str) -> Response:
    try:
        context = request._request.context

        case = Round.objects.get(slug=round_slug)
        team = Team.objects.get(team_name=TESTSOLVE_TEAM)

        Team.unlock_case(team, case, context.now)

        return Response({"status": "success"})
    except Exception as e:
        print(e)
        return Response({"error": "Could not unlock"}, status=404)


@api_view(["POST"])
@require_auth
def post_hint(request: Request, puzzle_slug: str) -> Response:
    try:
        context = request._request.context
        puzzle = context.team.unlocks.get(puzzle_slug)

        if request.data["followup"] == -1:
            # Ensure they have enough hints left
            if context.team.num_hints_remaining <= 0:
                return Response({"error": "No hints remaining"}, status=400)

        if puzzle is None:
            if context.is_admin:
                puzzle = Puzzle.objects.get(slug=puzzle_slug)
            else:
                raise Puzzle.DoesNotExist

        # Ensure request.data is not empty and contains all required fields
        required_fields = ["question", "followup"]
        if not isinstance(request.data, dict) or not all(
            field in request.data for field in required_fields
        ):
            raise KeyError

        if request.data["followup"] != -1:
            og_hint = Hint.objects.filter(
                puzzle=puzzle, team=context.team, id=request.data["followup"]
            ).first()
            if og_hint is None:
                return Response({"error": "Original hint not found"}, status=404)

            if og_hint.is_followed_up_on:
                return Response(
                    {"error": "Original hint already followed up to"}, status=400
                )

            og_hint.is_followed_up_on = True
            og_hint.save()

        hint = Hint.objects.create(
            puzzle=puzzle,
            team=context.team,
            is_followup=request.data["followup"] != -1,
            hint_question=request.data["question"],
        )

        serializer = HintSerializer(hint)

        return Response(serializer.data)
    except Puzzle.DoesNotExist:
        return Response({"error": "Puzzle not found"}, status=404)
    except KeyError:
        return Response(
            {"error": f"Missing required fields {required_fields}"}, status=400
        )


@api_view(["POST"])
@require_auth
def submit_event_answer(request: Request) -> Response:
    try:
        context = request._request.context
        event_slug = request.data["event_slug"]
        answer = request.data["answer"]

        event = Event.objects.get(slug=event_slug)

        sanitized_answer = "".join(
            [char for char in event.answer if char.isalpha()]
        ).upper()

        correct = Puzzle.normalize_answer(answer) == sanitized_answer

        if correct:
            EventCompletion.objects.create(
                team=context.team, event=event, completion_datetime=context.now
            )

        return Response(
            {"status": "correct" if correct else "incorrect", "correct": correct},
            status=200,
        )
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)


@api_view(["POST"])
@require_auth
def voucher_case(request: Request, round_slug: str) -> Response:
    try:
        django_context = request._request.context
        request_context = request.context

        case = Round.objects.get(slug=round_slug)
        case_meta = case.meta

        team = django_context.team

        if team.num_free_answers_remaining <= 0:
            return Response({"error": "No free answers remaining"}, status=400)

        if case_meta.slug in team.solves:
            return Response({"error": "Case already solved."}, status=400)

        if case_meta.slug not in team.unlocks:
            # If the puzzle is not unlocked, unlock it
            unlock = PuzzleUnlock.objects.create(
                team=team, puzzle=case_meta, unlock_datetime=request_context.now
            )
            unlock.save()

        answer = case_meta.answer
        return handle_answer(
            answer, request_context, django_context, case_meta.slug, voucher=True
        )
    except Exception as e:
        print(e)
        tb = traceback.format_exc()
        print(tb)
        return Response({"error": "Could not voucher"}, status=404)
