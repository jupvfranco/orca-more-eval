-module(response).
-mode(compile).

% -compile(export_all).
-export([main/1]).

build(1) -> {nil, nil};
build(D) -> {build(D-1), build(D-1)}.

count({nil, nil}) -> 1;
count({L, R}) -> 1 + count(L) + count(R).

reaper(0) ->
  ok;
reaper(N) ->
  receive {done, Id, Depth, Diffs} -> ok end,
  [io:format("(~p, ~p, ~p)~n",
             [Id, Depth, erlang:convert_time_unit(Diff, native, micro_seconds)])
   || Diff <- lists:reverse(Diffs)],
  reaper(N-1).

server(Id, NRequests, Depth) ->
  receive {start, StartTime} -> ok end,
  server_loop(Id, StartTime, NRequests, Depth, []).

server_loop(Id, _StartTime, 0, Depth, Diffs) ->
  main ! {done, Id, Depth, Diffs};
server_loop(Id, StartTime, NRequests, Depth, Diffs) ->
  count(build(Depth)),
  NewDiffs = [(erlang:monotonic_time() - StartTime)|Diffs],
  server_loop(Id, StartTime, NRequests-1, Depth, NewDiffs).

main(Args) ->
  register(main, self()),
  [NServers, NRequests, DepthMin, DepthMax] =
    lists:map(fun erlang:list_to_integer/1, Args),
  Depths = list_to_tuple(lists:seq(DepthMin, DepthMax, 2)),
  DepthSize = tuple_size(Depths),
  Servers =
    [
     begin
       Depth = element((Id rem DepthSize)+1, Depths),
       spawn(fun () -> server(Id, NRequests, Depth) end)
     end
     || Id <- lists:seq(0, NServers-1)],
  StartTime = erlang:monotonic_time(),
  [S ! {start, StartTime} || S <- Servers],
  reaper(NServers),
  ok.
