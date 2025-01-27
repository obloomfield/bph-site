from django.urls import path

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from puzzles.api import api_views, api_actions

from . import nyt_games_api
from . import data_mc_api
from . import soc_ded_api
from . import wordle_api
from . import letterboxed_api


@api_view(["GET"])
def index(request: Request) -> Response:
    return Response({"Puzzle": "Handlers"})


urlpatterns = [
    path("", index, name="index"),
    # HELPERS FOR SPECIFIC PUZZLES CAN GO HERE. TRY TO MAKE THE SLUGS MATCH THE PUZZLE SLUGS.
    # (for instance, if working on puzzle [slug])
    # path("[slug]/do-something", [slug]_api.do_something))
    #                                             ^---- each interactive puzzle should have its own [slug]_api.py file in this directory.
    path("<str:puzzle_slug>", api_views.get_puzzle, name="puzzle-index"),
    path(
        "<str:puzzle_slug>/submit",
        api_actions.submit_answer,
        name="puzzle-submit-answer",
    ),
    path(
        "nyt/connections-guess/<int:connection_round>/",
        nyt_games_api.index,
        name="nyt_connections_guess",
    ),
    path(
        "nyt/get-round-words/<int:connection_round>/",
        nyt_games_api.index,
        name="nyt_round_words",
    ),
    path(
        "nyt/connections-guess/<int:connection_round>/<str:selected_words>",
        nyt_games_api.check,
        name="nyt_connections_guess",
    ),
    path(
        "nyt/obituary-check",
        nyt_games_api.check_nyt_answers,
        name="obituary_check",
    ),
    path(
        "data/search/",
        data_mc_api.search_voice_recordings,
        name="search_voice_recordings",
    ),
    path(
        "data/fill_data",
        data_mc_api.admin_create_voice_recordings,
        name="admin_create_voice_recordings",
    ),
    path(
        "social-deduction/verdict_guess",
        soc_ded_api.verdict_guess,
        name="social_deduction_verdict_guess",
    ),
    path("wordle/verify-guess", wordle_api.verify_guess, name="verify-guess"),
    path("nyt/letterboxed", letterboxed_api.check, name="letterboxed"),
    path("nyt/letterboxed-final", letterboxed_api.checkall, name="letterboxed"),
]
