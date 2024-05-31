export default function Navbar() {
    return (
        <nav className="bg-green-600 p-4 top-0 p-4">
            <ul className="text-white flex text-2xl">
                <li className="mr-auto">
                <div className="flex items-center space-x-4">
                    <a className="font-bold" href="/">ChessGPT</a>
                    <a href="/leaderboard">Leaderboard</a>
                    <a href="/challenges">Challenges</a>
                    <a href="/settings">Settings</a>
                </div>
                </li>
                <li className="ml-auto">
                <div className="flex items-center space-x-4">
                    <>
                    <a href="/login">Log in</a>   
                    </>
                </div>
                </li>
            </ul>
        </nav>
    )
}