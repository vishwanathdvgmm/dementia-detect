import React from "react";
import { Activity, BrainCircuit } from "lucide-react";
import clsx from "clsx";

export default function RegionCard({ title, value, severity }) {
	const getSeverityColor = (sev) => {
		switch (sev) {
			case "high":
				return "text-red-400 bg-red-400/10 border-red-400/20";
			case "medium":
				return "text-amber-400 bg-amber-400/10 border-amber-400/20";
			case "low":
				return "text-teal-accent bg-teal-accent/10 border-teal-accent/20";
			default:
				return "text-slate-400 bg-navy-800 border-navy-700";
		}
	};

	return (
		<div
			className={clsx(
				"border p-4 rounded-lg flex items-center justify-between",
				getSeverityColor(severity),
			)}
		>
			<div className="flex items-center gap-3">
				<BrainCircuit className="w-5 h-5 opacity-70" />
				<div>
					<div className="text-xs font-semibold uppercase tracking-wider opacity-80">
						{title}
					</div>
					<div className="text-lg font-light mt-0.5">{value}</div>
				</div>
			</div>
			<Activity className="w-6 h-6 opacity-40" />
		</div>
	);
}
