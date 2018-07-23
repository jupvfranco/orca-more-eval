use "collections"
use "debug"

actor Main
    let _env: Env

    new create(env: Env) =>
        _env = env

        let print = try env.args(1).usize() else 0 end // Printing
        var body_qty = try env.args(2).usize() else 2 end // Number of bodies
        var steps = try env.args(3).usize() else 1 end // Number of steps

        World(body_qty, steps.u32(), _env, print).run_sim()
		World(body_qty, steps.u32(), _env, print).run_sim()
		World(body_qty, steps.u32(), _env, print).run_sim()