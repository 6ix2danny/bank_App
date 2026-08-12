
from fastapi import HTTPException

from app.models import branch as branch_model


def create_branch(payload):
    return branch_model.create_branch(payload.name, payload.address)


def list_branches():
    return branch_model.get_all_branches()


def get_branch(branch_id):
    branch = branch_model.get_branch(branch_id)
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


def update_branch(branch_id, payload):
    get_branch(branch_id)
    return branch_model.update_branch(branch_id, name=payload.name, address=payload.address)


def delete_branch(branch_id):
    get_branch(branch_id)
    branch_model.delete_branch(branch_id)
