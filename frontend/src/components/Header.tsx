// Universal Header
import type { JSX } from "react";
import { Link } from "react-router-dom";


export default function Header(): JSX.Element {
  return (
    <header>
        <nav>
            <Link to="/">Home</Link>
            <Link to="/signup">SignUp</Link>
            <Link to="/login-email">Login</Link>
            <Link to="/logout">Logout</Link>
        </nav>
    </header>
  )
}
