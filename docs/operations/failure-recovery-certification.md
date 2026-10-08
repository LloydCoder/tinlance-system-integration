# Failure, Replay and Recovery Certification

TSIC certifies recovery behavior as a contract. A retry is not considered safe merely because a transport can retry it: the operation must be idempotent or protected by a durable idempotency key. Security-context failures deny by default and emit audit evidence.