from unittest.mock import AsyncMock
import pytest
import asyncio

import fight

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'agent_move, expected',
    [
        (fight.Action(1), fight.Action(3)),
        (fight.Action(2), fight.Action(4)),
        (fight.Action(3), fight.Action(2)),
        (fight.Action(4), fight.Action(1)),
    ]
)
async def test_get_move(
    agent_move: fight.Action,
    expected: fight.Action,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    assert await fight.get_move(agent_move) == expected


@pytest.fixture
def agent() -> fight.Agent:
    return fight.Agent().__aiter__()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'agent_move, neo_move, agent_number, expected',
    [
        (fight.Action(1), fight.Action(3), 0,
         "Agent: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent Health: 5"),
        (fight.Action(2), fight.Action(4), 0,
         "Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 5"),
        (fight.Action(3), fight.Action(2), 0,
         "Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 5"),
        (fight.Action(4), fight.Action(1), 0,
         "Agent: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent Health: 5"),
        (fight.Action(4), fight.Action(1), 4,
         "Agent 4: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent Health: 5"),
    ]
)
async def test_print_move(
    agent_move: fight.Action,
    neo_move: fight.Action,
    agent_number: int,
    expected: str,
    agent: fight.Agent,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    await fight.print_move(agent, agent_move, neo_move, agent_number)
    captured = capsys.readouterr()
    assert expected in captured.out


@pytest.mark.asyncio
async def test_fight_with_one(
    agent: fight.Agent, 
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    captured = capsys.readouterr()
    await fight.fight_with_one(agent)
    assert all(str(i) in captured.out for i in range(agent.health))


@pytest.mark.asyncio
async def test_fight(
    agent: fight.Agent,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    monkeypatch.setattr(asyncio, "run", lambda x: x)
    await fight.fight()
    captured = capsys.readouterr()
    assert all(str(i) in captured.out for i in range(agent.health))
    assert "Neo wins" in captured.out


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "agent_number, health",
    [(5, -1), (2, 7), (10, -2)]
)
async def test_fightmany(
    agent_number: int,
    health: int,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    monkeypatch.setattr(asyncio, "run", lambda x: x)
    await fight.fightmany(agent_number)
    captured = capsys.readouterr()
    assert all(f"Agent {i}" in captured.out for i in range(1, agent_number+1))
    assert f"Health: {health}" not in captured.out
    assert "Neo wins" in captured.out
