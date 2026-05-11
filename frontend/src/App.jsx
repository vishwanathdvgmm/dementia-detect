import {
	BrowserRouter as Router,
	Routes,
	Route,
	Navigate,
} from "react-router-dom";
import Upload from "./pages/Upload";
import Viewer from "./pages/Viewer";
import Report from "./pages/Report";

function App() {
	return (
		<Router>
			<div className="min-h-screen bg-navy-900 font-sans flex flex-col">
				{/* Simple Header */}
				<header className="bg-navy-800 border-b border-navy-700 p-4 shadow-sm z-10">
					<div className="container mx-auto flex items-center justify-between">
						<div className="flex items-center gap-3">
							<div className="w-8 h-8 rounded bg-teal-accent flex items-center justify-center text-navy-900 font-bold">
								DD
							</div>
							<h1 className="text-xl font-semibold text-white tracking-wide">
								Dementia Detect
							</h1>
						</div>
						<div className="text-sm text-slate-400">
							Clinical Evaluation Mode
						</div>
					</div>
				</header>

				{/* Main Content Area */}
				<main className="flex-1 container mx-auto p-4 md:p-8 flex flex-col">
					<Routes>
						<Route
							path="/"
							element={<Navigate to="/upload" replace />}
						/>
						<Route path="/upload" element={<Upload />} />
						<Route path="/viewer/:scanId" element={<Viewer />} />
						<Route path="/report/:scanId" element={<Report />} />
					</Routes>
				</main>
			</div>
		</Router>
	);
}

export default App;
