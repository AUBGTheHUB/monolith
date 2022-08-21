### Tech Debt in Members:

- `members.jsx` is redundant - we can directly check the auth state in `render_members.jsx` with `Validate()` (as we do). Unfortunatelly, the current logic retrieves the members and passes them as a prop from `members.jsx` to `render_members.jsx` - easily fixable.
