import akka.actor.Actor
import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Props
import akka.util.Timeout
import akka.pattern.ask
import com.typesafe.config.Config
import com.typesafe.config.ConfigFactory
import com.typesafe.config.ConfigValueFactory
import com.typesafe.config.impl.ConfigLong
import scala.language.postfixOps
import scala.concurrent.duration._

final class Tree(left:Tree, right:Tree) {
  def count:Int = if (left eq null) 1 else 1 + left.count + right.count
}

object Tree {
  def apply(depth:Int):Tree = {
    if (depth > 1) new Tree(Tree(depth-1), Tree(depth-1))
    else new Tree(null, null)
  }
}

case class Start(start:Long)
case class Process(index:Int)
case class Finish(id:Int, depth:Int, diffs:Array[Long])

class Reaper(var countdown: Int) extends Actor {
  def receive: Actor.Receive = {
    case Finish(id, depth, diffs) => {
      countdown -= 1
      for (i <- 0 until diffs.length)
        println(s"(${id}, ${depth}, ${diffs(i)})")
      if (countdown == 0) {
        System.exit(0)
      }
    }
  }
}

class Server(id:Int, n_requests:Int, depth:Int) extends Actor {
  var start:Long = 0
  val diffs = new Array[Long](n_requests)

  def receive: Actor.Receive = {
    case Start(start) =>
      this.start = start
      self ! Process(0)
    case Process(index) => {
      if (index < n_requests) {
        Tree(depth).count
        diffs(index) = (System.nanoTime() - start)/1000
        self ! Process(index+1)
      } else {
        context.actorSelection("/user/reaper") ! Finish(id, depth, diffs)
      }
    }
  }
}

object Main {
  // val config =
  //   ConfigFactory.parseString(
  //       """
  //       akka{actor{default-dispatcher{fork-join-executor{parallelism-max = 1}}}}
  //       """
  //   )
  //   .withFallback(ConfigFactory.defaultReference(this.getClass.getClassLoader))

  // val system = ActorSystem("system",config)

  val system = ActorSystem("system")

  def main(args: Array[String]) {
    if (args.size < 4) {
      println("program <#server> <#requests>")
      System.exit(-1)
    }
    val n_servers = args(0).toInt
    val n_requests = args(1).toInt
    val depth_min = args(2).toInt
    val depth_max = args(3).toInt

    val depths = (depth_min to depth_max by 2).toArray

    val servers = (
        for (i <- 0 until n_servers)
          yield system.actorOf(
            Props(classOf[Server], i, n_requests, depths(i%depths.size)),
            "server_" + i)
        )

    system.actorOf(Props(classOf[Reaper], n_servers), "reaper")

    val start = Start(System.nanoTime())
    for (s <- servers)
      s ! start
  }
}
