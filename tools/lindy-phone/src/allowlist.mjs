// The allowlist is the security model of the whole gateway:
// exactly one inbound sender is answered — the owner. Everything else is
// logged (number masked) and silently ignored. No exceptions, no commands
// from strangers, no opt-in flow: the only user is the owner himself.

export function isOwner(from, ownerNumber) {
  return typeof from === "string" && from === ownerNumber;
}
