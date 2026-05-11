import React from "react";

export default function ScanViewer({ imageUrl, title }) {
	return (
		<div className="bg-black rounded-lg overflow-hidden border border-navy-700 relative flex items-center justify-center aspect-square shadow-lg">
			<div className="absolute top-2 left-2 px-2 py-1 bg-black/60 rounded text-xs text-white z-10 font-mono tracking-wider">
				{title}
			</div>

			{imageUrl ? (
				<img
					src={imageUrl}
					alt={title}
					className="w-full h-full object-contain mix-blend-screen"
				/>
			) : (
				<div className="text-navy-700 font-mono">No image data</div>
			)}

			{/* Clinical overlay metrics */}
			<div className="absolute bottom-2 right-2 text-[10px] text-slate-500 font-mono text-right pointer-events-none">
				<div>W: 1024 L: 512</div>
				<div>Zoom: 1.0x</div>
				<div>Axial T1</div>
			</div>
		</div>
	);
}
