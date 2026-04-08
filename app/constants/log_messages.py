# ── Auth ──────────────────────────────────────────────────────────────────────
AUTH_SUCCESS            = "Auth success | user={sub} ip={ip}"
AUTH_FAILED             = "Auth failed | ip={ip} reason={reason}"
AUTH_INVALID_TOKEN      = "Invalid token | ip={ip}"
AUTH_EXPIRED_TOKEN      = "Expired token | ip={ip}"
AUTH_MISSING_TOKEN      = "Missing token | ip={ip}"
AUTH_USER_NOT_FOUND     = "Authenticated user not found | sub={sub}"

# ── Request ───────────────────────────────────────────────────────────────────
REQUEST_RECEIVED        = "Request received | method={method} path={path} ip={ip}"
REQUEST_COMPLETED       = "Request completed | method={method} path={path} status={status} duration={duration}ms"
REQUEST_FAILED          = "Request failed | method={method} path={path} status={status}"

# ── User ──────────────────────────────────────────────────────────────────────
USER_CREATED            = "User created | user_id={user_id} email={email}"
USER_UPDATED            = "User updated | user_id={user_id}"
USER_DELETED            = "User deleted | user_id={user_id}"
USER_NOT_FOUND          = "User not found | user_id={user_id}"
USER_ALREADY_EXISTS     = "User already exists | email={email}"
USER_LOGIN              = "User login | user_id={user_id} ip={ip}"
USER_LOGOUT             = "User logout | user_id={user_id}"
USER_PASSWORD_CHANGED   = "Password changed | user_id={user_id}"

# ── Profile ───────────────────────────────────────────────────────────────────
PROFILE_VIEWED          = "Profile viewed | user_id={user_id}"
PROFILE_UPDATED         = "Profile updated | user_id={user_id}"
PROFILE_PICTURE_UPDATED = "Profile picture updated | user_id={user_id}"
PROFILE_NOT_FOUND       = "Profile not found | user_id={user_id}"

# ── Session ───────────────────────────────────────────────────────────────────
SESSION_CREATED         = "Session created | session_id={session_id} user_id={user_id}"
SESSION_EXPIRED         = "Session expired | session_id={session_id}"
SESSION_REVOKED         = "Session revoked | session_id={session_id} user_id={user_id}"
SESSION_NOT_FOUND       = "Session not found | session_id={session_id}"

# ── Database ──────────────────────────────────────────────────────────────────
DB_CONNECTED            = "Database connected | host={host}"
DB_CONNECTION_FAILED    = "Database connection failed | host={host} error={error}"
DB_QUERY_FAILED         = "Database query failed | model={model} error={error}"
DB_TRANSACTION_COMMIT   = "Transaction committed"
DB_TRANSACTION_ROLLBACK = "Transaction rolled back | error={error}"

# ── General ───────────────────────────────────────────────────────────────────
UNEXPECTED_ERROR        = "Unexpected error | error={error}"
SERVICE_STARTING        = "Service starting | env={env}"
SERVICE_READY           = "Service ready"
SERVICE_SHUTTING_DOWN   = "Service shutting down"
VALIDATION_ERROR        = "Validation error | path={path} detail={detail}"
RATE_LIMIT_EXCEEDED     = "Rate limit exceeded | ip={ip} path={path}"

