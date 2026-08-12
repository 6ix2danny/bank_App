
from typing import List

from fastapi import APIRouter

from app.models.schemas import BranchCreate, BranchOut, BranchUpdate
from app.services import branch_service

router = APIRouter(prefix="/branches", tags=["branches"])


@router.post("", response_model=BranchOut, status_code=201)
def create_branch(payload: BranchCreate):
    return BranchOut(**vars(branch_service.create_branch(payload)))


@router.get("", response_model=List[BranchOut])
def list_branches():
    return [BranchOut(**vars(b)) for b in branch_service.list_branches()]


@router.get("/{branch_id}", response_model=BranchOut)
def get_branch(branch_id: int):
    return BranchOut(**vars(branch_service.get_branch(branch_id)))


@router.put("/{branch_id}", response_model=BranchOut)
def update_branch(branch_id: int, payload: BranchUpdate):
    return BranchOut(**vars(branch_service.update_branch(branch_id, payload)))


@router.delete("/{branch_id}", status_code=204)
def delete_branch(branch_id: int):
    branch_service.delete_branch(branch_id)
    return None
