import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Download, FileText, CheckCircle } from "lucide-react";

export default function Report() {
	const { scanId } = useParams();
	const navigate = useNavigate();
	const [downloading, setDownloading] = useState(false);

	const handleDownload = async () => {
		setDownloading(true);
		try {
			const filename = sessionStorage.getItem(`scan_${scanId}`);
			if (!filename) throw new Error("No scan found");

			const response = await fetch(
				`http://localhost:8000/api/report/${filename}`,
			);
			if (!response.ok) throw new Error("Failed to generate report");

			const blob = await response.blob();
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement("a");
			a.href = url;
			a.download = `Dementia_Detect_Report_${scanId ? scanId.substring(0, 8) : "unknown"}.pdf`;
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
		} catch (err) {
			console.error(err);
			alert("Failed to download the PDF report.");
		} finally {
			setDownloading(false);
		}
	};

	return (
		<div className="flex-1 flex flex-col items-center justify-center max-w-3xl mx-auto w-full">
			<div className="w-full mb-8">
				<button
					onClick={() => navigate(`/viewer/${scanId}`)}
					className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
				>
					<ArrowLeft className="w-4 h-4" /> Back to Viewer
				</button>
			</div>

			<div className="bg-navy-800 border border-navy-700 rounded-xl p-8 w-full shadow-xl">
				<div className="flex items-center gap-4 mb-8 pb-6 border-b border-navy-700">
					<div className="w-16 h-16 bg-teal-accent/10 rounded-full flex items-center justify-center border border-teal-accent/30">
						<FileText className="w-8 h-8 text-teal-accent" />
					</div>
					<div>
						<h2 className="text-2xl font-light text-white">
							Clinical Assessment Report
						</h2>
						<p className="text-slate-400 font-mono text-sm mt-1">
							ID:{" "}
							{scanId
								? scanId.substring(0, 8).toUpperCase()
								: "UNKNOWN"}
						</p>
					</div>
				</div>

				<div className="space-y-6 mb-10">
					<h3 className="text-lg font-medium text-slate-200">
						Included in the final PDF:
					</h3>

					<ul className="space-y-4">
						{[
							"Patient Details & Scan Metadata",
							"Primary Model Prediction & Confidence Scores",
							"GradCAM ROI Visualizations (Hippocampus & Entorhinal Cortex)",
							"CDR Staging Estimate & Findings Summary",
						].map((item, i) => (
							<li key={i} className="flex items-start gap-3">
								<CheckCircle className="w-5 h-5 text-teal-accent flex-shrink-0 mt-0.5" />
								<span className="text-slate-300">{item}</span>
							</li>
						))}
					</ul>
				</div>

				<div className="flex justify-end pt-6 border-t border-navy-700">
					<button
						onClick={handleDownload}
						disabled={downloading}
						className="flex items-center gap-2 px-6 py-3 bg-teal-accent hover:bg-teal-accent/90 text-navy-900 font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{downloading ? (
							<>Generating PDF...</>
						) : (
							<>
								<Download className="w-5 h-5" /> Export PDF
								Report
							</>
						)}
					</button>
				</div>
			</div>
		</div>
	);
}
