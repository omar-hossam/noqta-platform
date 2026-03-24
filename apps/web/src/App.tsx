import { Route, Switch, Link } from "wouter";
import { Home } from "./pages/Home";
import { About } from "./pages/About";
import { Page404 } from "./pages/404";

export default function App() {
  return (
    <main>
      <nav className="flex gap-10">
        <Link href="/">Home</Link>
        <Link href="/about">About</Link>
        <Link href="/asdewqeqwe">Not Found</Link>
      </nav>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/about" component={About} />

        <Route path="*" component={Page404}></Route>
      </Switch>
    </main>
  )
}
