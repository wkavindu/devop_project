from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from pymongo import DESCENDING
from pymongo.errors import PyMongoError

from .db import get_client, get_db


bp = Blueprint("main", __name__)
SEVERITIES = ("Low", "Medium", "High", "Critical")
STATUSES = ("Open", "Investigating", "Resolved")


def _collection():
    return get_db().incidents


def _incident_id(value):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        abort(404)


def _form_data():
    data = {
        "title": request.form.get("title", "").strip(),
        "service": request.form.get("service", "").strip(),
        "description": request.form.get("description", "").strip(),
        "severity": request.form.get("severity", ""),
        "status": request.form.get("status", ""),
    }
    if not data["title"] or not data["service"] or not data["description"]:
        return data, "Title, affected service, and description are required."
    if data["severity"] not in SEVERITIES or data["status"] not in STATUSES:
        return data, "Choose a valid severity and status."
    return data, None


@bp.get("/")
def index():
    try:
        incidents = list(_collection().find().sort("created_at", DESCENDING))
    except PyMongoError:
        incidents = []
        flash("MongoDB is unavailable. Start it and refresh the page.", "danger")
    counts = {status: sum(item.get("status") == status for item in incidents) for status in STATUSES}
    return render_template("index.html", incidents=incidents, counts=counts)


@bp.route("/incidents/new", methods=("GET", "POST"))
def create_incident():
    incident = {"severity": "Medium", "status": "Open"}
    if request.method == "POST":
        incident, error = _form_data()
        if not error:
            now = datetime.now(timezone.utc)
            incident.update(created_at=now, updated_at=now)
            try:
                result = _collection().insert_one(incident)
                flash("Incident created successfully.", "success")
                return redirect(url_for("main.incident_detail", incident_id=result.inserted_id))
            except PyMongoError:
                error = "Could not save the incident because MongoDB is unavailable."
        flash(error, "danger")
    return render_template("form.html", incident=incident, action="Create")


@bp.get("/incidents/<incident_id>")
def incident_detail(incident_id):
    incident = _collection().find_one({"_id": _incident_id(incident_id)})
    if incident is None:
        abort(404)
    return render_template("detail.html", incident=incident)


@bp.route("/incidents/<incident_id>/edit", methods=("GET", "POST"))
def edit_incident(incident_id):
    object_id = _incident_id(incident_id)
    incident = _collection().find_one({"_id": object_id})
    if incident is None:
        abort(404)
    if request.method == "POST":
        form_data, error = _form_data()
        if not error:
            form_data["updated_at"] = datetime.now(timezone.utc)
            _collection().update_one({"_id": object_id}, {"$set": form_data})
            flash("Incident updated successfully.", "success")
            return redirect(url_for("main.incident_detail", incident_id=object_id))
        incident.update(form_data)
        flash(error, "danger")
    return render_template("form.html", incident=incident, action="Update")


@bp.post("/incidents/<incident_id>/delete")
def delete_incident(incident_id):
    result = _collection().delete_one({"_id": _incident_id(incident_id)})
    if result.deleted_count == 0:
        abort(404)
    flash("Incident deleted.", "success")
    return redirect(url_for("main.index"))


@bp.get("/health")
def health():
    return jsonify(status="healthy", service="opstrack"), 200


@bp.get("/ready")
def ready():
    try:
        get_client().admin.command("ping")
        return jsonify(status="ready", database="connected"), 200
    except PyMongoError:
        return jsonify(status="not ready", database="unavailable"), 503


@bp.app_errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@bp.app_context_processor
def inject_choices():
    return {"severities": SEVERITIES, "statuses": STATUSES}
