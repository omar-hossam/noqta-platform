import { Route, Switch, Link } from 'wouter';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <>
      <header>
        <h1 font='header'>نقطة <i class="i-ph-drop text-blue-400" /></h1>
      </header>
      <main bg="brand-bg" text="brand-text" font='body' >
        
        <Switch>
        
          <Route path='/' component={Home} />
          <Route path='/login' component={Login} />
          <Route path='/signup' component={Signup} />
          <Route path='/profile' component={Profile} />
          
          <Route> <NotFound /> </Route>
        
        </Switch>
      </main>
    </>
  )
}
