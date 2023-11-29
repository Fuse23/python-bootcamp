import asyncio
from enum import Enum, auto
from random import choice
from typing import Coroutine


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:
    def __aiter__(self, health=5) -> 'Agent':
        self.health: int = health
        self.actions = list(Action)
        return self

    async def __anext__(self) -> Action:
        return choice(self.actions)


async def get_move(agent_move: Action) -> Action:
    await asyncio.sleep(0.2)
    if agent_move in (Action.HIGHKICK, Action.LOWKICK):
        return Action(agent_move.value + 2)
    return Action(5 - agent_move.value)


async def print_move(
        agent: Agent,
        agent_move: Action,
        neo_move: Action,
        agent_number: int = 0,
) -> None:
    await asyncio.sleep(0.2)
    print(
        f"Agent{' ' + str(agent_number) if agent_number > 0 else ''}"
        + f": {agent_move}, Neo: {neo_move}, Agent Health: {agent.health}"
    )


async def fight_with_one(agent: Agent, number: int = 0) -> None:
    async for agent_move in agent:
        if agent.health == 0:
            break
        neo_move: Action = await get_move(agent_move)
        if neo_move in (Action.HIGHKICK, Action.LOWKICK):
            agent.health -= 1
        await print_move(agent, agent_move, neo_move, number)


async def fight() -> None:
    agent: Agent = Agent()
    await fight_with_one(agent)
    print("Neo wins")


async def fightmany(n: int) -> None:
    agents: list[Agent] = [Agent() for _ in range(n)]
    tasks: list[Coroutine] = []
    for i in range(n):
        tasks.append(fight_with_one(agents[i], i+1))
    await asyncio.gather(*tasks)
    print("Neo wins")


if __name__ == "__main__":
    print("FIGHT WITH ONE")
    asyncio.run(fight())
    print("-------------------------------------\n")
    print("FIGHT WITH 5 AGENTS")
    asyncio.run(fightmany(5))
