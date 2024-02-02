export default function Navbar() {
    return (
        <nav className="bg-blue-800 p-4 sticky top-0 p-4">
            <ul className="text-white flex text-2xl font-bold">
                <li className="mr-auto">
                <div className="flex items-center space-x-4">
                    <a href="/">ChessGPT</a>
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