import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { UploadCloud, FileImage, Loader2, AlertCircle } from "lucide-react";
import clsx from "clsx";

export default function Upload() {
	const [isDragging, setIsDragging] = useState(false);
	const [isUploading, setIsUploading] = useState(false);
	const [error, setError] = useState(null);
	const navigate = useNavigate();

	const handleDragOver = useCallback((e) => {
		e.preventDefault();
		setIsDragging(true);
	}, []);

	const handleDragLeave = useCallback((e) => {
		e.preventDefault();
		setIsDragging(false);
	}, []);

	const uploadFile = async (file) => {
		if (!file) return;

		setIsUploading(true);
		setError(null);

		const formData = new FormData();
		formData.append("file", file);

		try {
			// Using full URL for simplicity since we're running locally.
			// In production, configure proxy in vite.config.js
			const response = await axios.post(
				"http://localhost:8000/api/upload",
				formData,
				{
					headers: { "Content-Type": "multipart/form-data" },
				},
			);

			const { scan_id, filename } = response.data;

			// Store filename in sessionStorage so the viewer knows what file to predict on
			sessionStorage.setItem(`scan_${scan_id}`, filename);

			// Navigate to viewer
			navigate(`/viewer/${scan_id}`);
		} catch (err) {
			console.error(err);
			setError(
				"Failed to upload scan. Please ensure the backend is running.",
			);
		} finally {
			setIsUploading(false);
		}
	};

	const handleDrop = useCallback((e) => {
		e.preventDefault();
		setIsDragging(false);
		const files = e.dataTransfer.files;
		if (files && files.length > 0) {
			uploadFile(files[0]);
		}
	}, []);

	const handleFileChange = (e) => {
		const files = e.target.files;
		if (files && files.length > 0) {
			uploadFile(files[0]);
		}
	};

	return (
		<div className="flex-1 flex flex-col items-center justify-center max-w-4xl mx-auto w-full">
			<div className="text-center mb-10">
				<h2 className="text-3xl font-light text-white mb-4">
					Acquire MRI Scan
				</h2>
				<p className="text-slate-400 max-w-lg mx-auto">
					Upload a high-resolution axial MRI slice for automated
					dementia progression analysis and GradCAM visualization.
				</p>
			</div>

			{error && (
				<div className="w-full max-w-2xl bg-red-900/20 border border-red-500/50 rounded-lg p-4 mb-6 flex items-start gap-3 text-red-200">
					<AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
					<p>{error}</p>
				</div>
			)}

			<div
				onDragOver={handleDragOver}
				onDragLeave={handleDragLeave}
				onDrop={handleDrop}
				className={clsx(
					"w-full max-w-2xl aspect-[16/9] border-2 border-dashed rounded-xl flex flex-col items-center justify-center p-8 transition-all duration-200 relative overflow-hidden",
					isDragging
						? "border-teal-accent bg-teal-accent/5"
						: "border-navy-700 bg-navy-800/50 hover:bg-navy-800 hover:border-navy-600",
				)}
			>
				<input
					type="file"
					accept="image/jpeg, image/png, image/jpg"
					onChange={handleFileChange}
					className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
					disabled={isUploading}
				/>

				{isUploading ? (
					<div className="flex flex-col items-center text-teal-accent">
						<Loader2 className="w-12 h-12 mb-4 animate-spin" />
						<p className="text-lg font-medium">
							Uploading and initializing analysis...
						</p>
					</div>
				) : (
					<div className="flex flex-col items-center text-slate-400 pointer-events-none">
						<div className="w-20 h-20 bg-navy-900 rounded-full flex items-center justify-center mb-6 shadow-inner border border-navy-700">
							<UploadCloud className="w-10 h-10 text-teal-accent" />
						</div>
						<p className="text-xl font-medium text-slate-200 mb-2">
							Drag and drop MRI scan here
						</p>
						<p className="text-sm mb-6">
							Supports JPG, PNG formats
						</p>
						<button className="px-6 py-2.5 bg-navy-700 hover:bg-navy-600 text-white rounded-md font-medium transition-colors border border-navy-600 focus:outline-none focus:ring-2 focus:ring-teal-accent/50 pointer-events-auto">
							Browse Files
						</button>
					</div>
				)}
			</div>

			{/* Demo Mode Action */}
			<div className="mt-8 flex flex-col items-center">
				<p className="text-slate-400 text-sm mb-3">
					No scans on hand? Try the system with a known positive case.
				</p>
				<button
					onClick={async () => {
						setIsUploading(true);
						try {
							const res = await fetch("/demo_scan.jpg");
							const blob = await res.blob();
							const file = new File([blob], "demo_scan.jpg", {
								type: "image/jpeg",
							});
							uploadFile(file);
						} catch (err) {
							console.error(err);
							setError("Failed to load demo scan.");
							setIsUploading(false);
						}
					}}
					disabled={isUploading}
					className="px-5 py-2 border border-teal-accent/50 text-teal-accent hover:bg-teal-accent hover:text-navy-900 font-medium rounded-full transition-colors text-sm flex items-center gap-2 disabled:opacity-50"
				>
					<UploadCloud className="w-4 h-4" /> Load Clinical Demo Scan
				</button>
			</div>

			<div className="mt-12 grid grid-cols-3 gap-6 w-full max-w-2xl">
				{[
					{
						icon: FileImage,
						title: "Standardized",
						desc: "Auto-resizes to 224x224",
					},
					{
						icon: FileImage,
						title: "Normalized",
						desc: "Applies ImageNet stats",
					},
					{
						icon: FileImage,
						title: "Secure",
						desc: "Processed locally on device",
					},
				].map((feature, i) => (
					<div
						key={i}
						className="bg-navy-800/30 border border-navy-700/50 p-4 rounded-lg flex flex-col items-center text-center"
					>
						<div className="w-10 h-10 rounded-full bg-navy-800 flex items-center justify-center mb-3">
							<feature.icon className="w-5 h-5 text-teal-accent/70" />
						</div>
						<h4 className="text-sm font-medium text-slate-200 mb-1">
							{feature.title}
						</h4>
						<p className="text-xs text-slate-500">{feature.desc}</p>
					</div>
				))}
			</div>
		</div>
	);
}
