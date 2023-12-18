import { z } from "zod";

const contextSchema = z.object({
  team: z
    .object({
      team_name: z.string(),
      total_hints_awarded: z.number().int(),
      num_hints_remaining: z.number().int(),
      total_free_answers_awarded: z.number().int(),
      num_free_answers_remaining: z.number().int(),
      is_prerelease_testsolver: z.boolean(),
      brown_members: z.boolean(),
      in_person: z.boolean(),
    })
    .optional(),
  unlocks: z.record(z.string().transform((x) => new Date(x))),
  rounds: z.record(z.string().transform((x) => new Date(x))),
  // TODO: make this work with minor case / major case system
  // TODO: also add events as separate.

  // nice-to-have extras from Context
  is_admin: z.boolean(),
  is_superuser: z.boolean(),
  
  // all from BaseContext
  now: z.string().transform((x) => new Date(x)),
  start_time: z.string().transform((x) => new Date(x)),
  time_since_start: z.string().transform((x) => new Date(x)),
  end_time: z.string().transform((x) => new Date(x)),
  close_time: z.string().transform((x) => new Date(x)),
  solution_time: z.string().transform((x) => new Date(x)),
  hunt_is_prereleased: z.boolean(),
  hunt_has_started: z.boolean(),
  hunt_has_almost_started: z.boolean(),
  hunt_is_over: z.boolean(),
  hunt_is_closed: z.boolean(),
  hunt_solutions_open: z.boolean(),
  num_metas: z.number().int(),
});

// @ts-expect-error djangoContext is defined in the template html
export const context = contextSchema.parse(djangoContext);
