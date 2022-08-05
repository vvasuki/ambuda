from flask import (
    Blueprint,
    abort,
    render_template,
)

import ambuda.queries as q
from ambuda import database as db
from ambuda.utils.auth import admin_required


bp = Blueprint("users", __name__)


@bp.route("/<username>/")
def user(username):
    user_ = q.user(username)
    if not user_:
        abort(404)

    session = q.get_session()
    return render_template(
        "proofing/user.html",
        user=user_,
    )


@bp.route("/<username>/edits")
def user_edits(username):
    user_ = q.user(username)
    if not user_:
        abort(404)

    session = q.get_session()
    user_revisions = session.query(db.Revision).filter_by(author_id=user_.id).all()
    return render_template(
        "proofing/user-edits.html", user=user_, user_revisions=user_revisions
    )


@bp.route("/<username>/admin")
@admin_required
def user_admin(username):
    user_ = q.user(username)
    if not user_:
        abort(404)

    session = q.get_session()
    return render_template(
        "proofing/user-admin.html",
        user=user_,
    )
