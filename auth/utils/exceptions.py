from http import HTTPStatus

from api.v1.messages import TOKEN_EXPIRED, TOKEN_INVALID
from database.db import jwt
from database.redis_cache import redis_cache
from flask import jsonify


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    if jwt_payload["type"] == "access":
        jti = jwt_payload["jti"]
        token_in_redis = redis_cache.get(jti)
        return token_in_redis is not None


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload: dict):
    return jsonify({
        'status': 401,
        'sub_status': 101,
        'msg': TOKEN_EXPIRED
    }), HTTPStatus.OK


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "success": False,
        "message": TOKEN_INVALID,
        "description": "Signature verification failed.",
        "errors": [],
    }), HTTPStatus.FORBIDDEN


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload: dict):
    return jsonify({
        "success": False,
        "message": TOKEN_INVALID,
        "description": "Token has been revoked",
        "errors": [],
    }), HTTPStatus.FORBIDDEN
