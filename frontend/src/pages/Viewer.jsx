import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { Loader2, ArrowLeft, Layers, FileOutput } from "lucide-react";
import ScanViewer from "../components/ScanViewer";
import RiskGauge from "../components/RiskGauge";
import RegionCard from "../components/RegionCard";

export default function Viewer() {
	const { scanId } = useParams();
	const navigate = useNavigate();

	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	const [data, setData] = useState(null);
	const [showHeatmap, setShowHeatmap] = useState(true);

	const filename = sessionStorage.getItem(`scan_${scanId}`);

	useEffect(() => {
		if (!filename) {
			navigate("/upload");
			return;
		}

		const fetchPrediction = async () => {
			try {
				const response = await axios.post(
					"http://localhost:8000/api/predict",
					{
						filename: filename,
					},
				);
				setData(response.data);
			} catch (err) {
				console.error(err);
				setError("Failed to process the scan.");
			} finally {
				setLoading(false);
			}
		};

		fetchPrediction();
	}, [filename, scanId, navigate]);

	if (loading) {
		return (
			<div className="flex-1 flex flex-col items-center justify-center">
				<Loader2 className="w-12 h-12 text-teal-accent animate-spin mb-4" />
				<h2 className="text-xl text-white font-light">
					Analyzing Scan via EfficientNet-B4...
				</h2>
				<p className="text-slate-400 mt-2">
					Running preprocessing and GradCAM generation
				</p>
			</div>
		);
	}

	if (error) {
		return (
			<div className="flex-1 flex flex-col items-center justify-center">
				<div className="text-red-400 text-xl">{error}</div>
				<button
					onClick={() => navigate("/upload")}
					className="mt-4 text-teal-accent hover:underline"
				>
					Return to Upload
				</button>
			</div>
		);
	}

	const origUrl = `http://localhost:8000/static/uploads/${filename}`;
	const heatmapUrl = `http://localhost:8000${data.heatmap_url}`;

	// Determine severity based on prediction
	const getSeverity = (cls) => {
		if (cls === "ModerateDemented") return "high";
		if (cls === "MildDemented") return "medium";
		if (cls === "VeryMildDemented") return "medium";
		return "low";
	};

	const severity = getSeverity(data.predicted_class);

	return (
		<div className="flex-1 flex flex-col w-full h-full">
			<div className="flex items-center justify-between mb-6">
				<button
					onClick={() => navigate("/upload")}
					className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
				>
					<ArrowLeft className="w-4 h-4" /> New Scan
				</button>

				<div className="flex items-center gap-4">
					<button
						onClick={() => setShowHeatmap(!showHeatmap)}
						className={`flex items-center gap-2 px-4 py-2 rounded border transition-colors ${showHeatmap ? "bg-navy-700 border-teal-accent text-white" : "bg-navy-800 border-navy-600 text-slate-400 hover:bg-navy-700"}`}
					>
						<Layers className="w-4 h-4" /> Toggle Heatmap
					</button>

					<button
						onClick={() => navigate(`/report/${scanId}`)}
						className="flex items-center gap-2 px-4 py-2 bg-teal-accent hover:bg-teal-accent/90 text-navy-900 font-medium rounded transition-colors"
					>
						<FileOutput className="w-4 h-4" /> Generate Report
					</button>
				</div>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
				{/* Left Column: Viewer */}
				<div className="lg:col-span-2 bg-navy-800/30 border border-navy-700 rounded-xl p-4 flex flex-col">
					<h2 className="text-lg font-medium text-white mb-4">
						Axial MRI Viewer
					</h2>
					<div className="flex-1 min-h-0 relative">
						<ScanViewer
							imageUrl={showHeatmap ? heatmapUrl : origUrl}
							title={
								showHeatmap
									? "GradCAM Overlay (Target: Hippocampus)"
									: "Original Input (224x224)"
							}
						/>
					</div>
				</div>

				{/* Right Column: Analytics */}
				<div className="flex flex-col gap-6 overflow-y-auto">
					{/* Main Prediction */}
					<div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
						<h3 className="text-slate-400 text-sm font-medium mb-1 uppercase tracking-wider">
							Primary Diagnosis
						</h3>
						<div
							className={`text-3xl font-light mb-2 ${severity === "high" ? "text-red-400" : severity === "medium" ? "text-amber-400" : "text-teal-accent"}`}
						>
							{data.predicted_class}
						</div>
						<div className="text-slate-300">
							Confidence:{" "}
							<span className="font-mono ml-1 text-white">
								{(data.confidence * 100).toFixed(1)}%
							</span>
						</div>
					</div>

					{/* Regional Analysis */}
					<div className="flex flex-col gap-3">
						<RegionCard
							title="Hippocampal Volume"
							value={
								severity === "high"
									? "Severe Atrophy"
									: severity === "medium"
										? "Mild Atrophy"
										: "Normal"
							}
							severity={severity}
						/>
						<RegionCard
							title="Ventricle Expansion"
							value={
								severity === "high"
									? "Enlarged"
									: "Normal Limits"
							}
							severity={severity === "high" ? "medium" : "low"}
						/>
					</div>

					{/* Probability Gauge */}
					<div className="bg-navy-800/50 border border-navy-700 rounded-xl p-4 flex-1 min-h-[300px]">
						<RiskGauge probabilities={data.probabilities} />
					</div>
				</div>
			</div>
		</div>
	);
}
