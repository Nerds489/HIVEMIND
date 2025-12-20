"""
HIVEMIND Agent Routes

API endpoints for agent and team information.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hivemind.agents.pool import AgentPool, get_agent_pool
from hivemind.agents.teams import TeamID
from hivemind.api.dependencies import get_current_user
from hivemind.api.schemas import (
    AgentResponse,
    AgentStateResponse,
    TeamResponse,
    TeamWithAgents,
)
from hivemind.observability import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Agents"])


# =============================================================================
# Agent Endpoints
# =============================================================================

@router.get(
    "/v1/agents",
    response_model=list[AgentResponse],
    summary="List all agents",
    description="Retrieve information about all 24 agents in the HIVEMIND system",
)
async def list_agents(
    team: str | None = None,
    available_only: bool = False,
    agent_pool: AgentPool = Depends(get_agent_pool),
    current_user: str | None = Depends(get_current_user),
) -> list[AgentResponse]:
    """
    List all agents.

    Args:
        team: Optional filter by team ID (DEV, SEC, INF, QA)
        available_only: Only return available agents
        agent_pool: Agent pool dependency
        current_user: Current user (if authenticated)

    Returns:
        List of agents
    """
    # Get agents
    if team:
        try:
            team_id = TeamID(team.upper())
            agents = agent_pool.get_agents_by_team(team_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid team ID: {team}. Must be one of: DEV, SEC, INF, QA",
            )
    else:
        agents = list(agent_pool.agents.values())

    # Filter by availability
    if available_only:
        agents = [a for a in agents if a.is_available]

    # Convert to response models
    return [
        AgentResponse(
            id=agent.id,
            name=agent.metadata.name,
            team=agent.team,
            description=agent.metadata.description,
            state=AgentStateResponse(agent.state.value),
            capabilities=[c.value for c in agent.metadata.capabilities],
            keywords=agent.metadata.keywords,
            current_task_id=agent.current_task_id,
            total_tasks_completed=agent.total_tasks_completed,
            total_tasks_failed=agent.total_tasks_failed,
            is_available=agent.is_available,
        )
        for agent in agents
    ]


@router.get(
    "/v1/agents/{agent_id}",
    response_model=AgentResponse,
    summary="Get agent details",
    description="Retrieve detailed information about a specific agent",
)
async def get_agent(
    agent_id: str,
    agent_pool: AgentPool = Depends(get_agent_pool),
    current_user: str | None = Depends(get_current_user),
) -> AgentResponse:
    """
    Get agent details.

    Args:
        agent_id: Agent ID (e.g., DEV-001, SEC-002)
        agent_pool: Agent pool dependency
        current_user: Current user (if authenticated)

    Returns:
        Agent information

    Raises:
        HTTPException: If agent not found
    """
    agent = agent_pool.get_agent(agent_id)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent not found: {agent_id}",
        )

    return AgentResponse(
        id=agent.id,
        name=agent.metadata.name,
        team=agent.team,
        description=agent.metadata.description,
        state=AgentStateResponse(agent.state.value),
        capabilities=[c.value for c in agent.metadata.capabilities],
        keywords=agent.metadata.keywords,
        current_task_id=agent.current_task_id,
        total_tasks_completed=agent.total_tasks_completed,
        total_tasks_failed=agent.total_tasks_failed,
        is_available=agent.is_available,
    )


# =============================================================================
# Team Endpoints
# =============================================================================

@router.get(
    "/v1/teams",
    response_model=list[TeamResponse],
    summary="List all teams",
    description="Retrieve information about all 4 teams in the HIVEMIND system",
)
async def list_teams(
    agent_pool: AgentPool = Depends(get_agent_pool),
    current_user: str | None = Depends(get_current_user),
) -> list[TeamResponse]:
    """
    List all teams.

    Args:
        agent_pool: Agent pool dependency
        current_user: Current user (if authenticated)

    Returns:
        List of teams
    """
    teams = list(agent_pool.teams.values())

    return [
        TeamResponse(
            id=team.id.value,
            name=team.name,
            description=team.config.description,
            keywords=team.config.keywords,
            agent_count=team.size,
            available_agents=len(team.available_agents),
            availability=team.availability,
        )
        for team in teams
    ]


@router.get(
    "/v1/teams/{team_id}",
    response_model=TeamWithAgents,
    summary="Get team details",
    description="Retrieve detailed information about a specific team and its agents",
)
async def get_team(
    team_id: str,
    include_agents: bool = True,
    agent_pool: AgentPool = Depends(get_agent_pool),
    current_user: str | None = Depends(get_current_user),
) -> TeamWithAgents:
    """
    Get team details.

    Args:
        team_id: Team ID (DEV, SEC, INF, QA)
        include_agents: Whether to include agent details
        agent_pool: Agent pool dependency
        current_user: Current user (if authenticated)

    Returns:
        Team information with agents

    Raises:
        HTTPException: If team not found
    """
    try:
        team_enum = TeamID(team_id.upper())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid team ID: {team_id}. Must be one of: DEV, SEC, INF, QA",
        )

    team = agent_pool.get_team(team_enum)

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team not found: {team_id}",
        )

    # Convert agents
    agents = []
    if include_agents:
        agents = [
            AgentResponse(
                id=agent.id,
                name=agent.metadata.name,
                team=agent.team,
                description=agent.metadata.description,
                state=AgentStateResponse(agent.state.value),
                capabilities=[c.value for c in agent.metadata.capabilities],
                keywords=agent.metadata.keywords,
                current_task_id=agent.current_task_id,
                total_tasks_completed=agent.total_tasks_completed,
                total_tasks_failed=agent.total_tasks_failed,
                is_available=agent.is_available,
            )
            for agent in team.agents
        ]

    return TeamWithAgents(
        id=team.id.value,
        name=team.name,
        description=team.config.description,
        keywords=team.config.keywords,
        agent_count=team.size,
        available_agents=len(team.available_agents),
        availability=team.availability,
        agents=agents,
    )


# =============================================================================
# Agent Discovery Endpoints
# =============================================================================

@router.get(
    "/v1/agents/search",
    response_model=list[AgentResponse],
    summary="Search for agents",
    description="Find agents that can handle specific keywords or capabilities",
)
async def search_agents(
    keywords: str | None = None,
    capability: str | None = None,
    available_only: bool = True,
    limit: int = 10,
    agent_pool: AgentPool = Depends(get_agent_pool),
    current_user: str | None = Depends(get_current_user),
) -> list[AgentResponse]:
    """
    Search for agents by keywords or capabilities.

    Args:
        keywords: Comma-separated keywords to search for
        capability: Specific capability to filter by
        available_only: Only return available agents
        limit: Maximum number of results
        agent_pool: Agent pool dependency
        current_user: Current user (if authenticated)

    Returns:
        List of matching agents
    """
    if not keywords and not capability:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either keywords or capability parameter",
        )

    # Search by keywords
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(",")]
        agents = agent_pool.find_agents_by_keywords(keyword_list)
    else:
        # Filter by capability
        agents = [
            agent
            for agent in agent_pool.agents.values()
            if capability.lower() in [c.value for c in agent.metadata.capabilities]
        ]

    # Filter by availability
    if available_only:
        agents = [a for a in agents if a.is_available]

    # Limit results
    agents = agents[:limit]

    return [
        AgentResponse(
            id=agent.id,
            name=agent.metadata.name,
            team=agent.team,
            description=agent.metadata.description,
            state=AgentStateResponse(agent.state.value),
            capabilities=[c.value for c in agent.metadata.capabilities],
            keywords=agent.metadata.keywords,
            current_task_id=agent.current_task_id,
            total_tasks_completed=agent.total_tasks_completed,
            total_tasks_failed=agent.total_tasks_failed,
            is_available=agent.is_available,
        )
        for agent in agents
    ]
