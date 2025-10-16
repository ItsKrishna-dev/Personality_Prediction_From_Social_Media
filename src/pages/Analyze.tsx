import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { PersonalityInput } from "@/components/PersonalityInput";
import { toast } from "sonner";

const API_URL = "http://localhost:8000";

interface TraitScore {
  score: number;
  percentage: number;
}

interface PredictionResponse {
  scores: Record<string, TraitScore>;
  interpretations: Record<string, string>;
  summary: {
    full_summary?: string;
    strengths?: string;
    growth_areas?: string;
    career_suggestions?: string;
  };
  success: boolean;
}

const Analyze = () => {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (comments: string[]) => {
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          comments,
          include_summary: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: PredictionResponse = await response.json();
      
      if (data.success) {
        toast.success("Personality analysis complete!");
        // Navigate to results page with the data
        navigate("/results", { state: { results: data } });
      } else {
        throw new Error("Analysis failed");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Failed to analyze personality. Make sure the backend is running on http://localhost:8000");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full flex items-center justify-center">
        <PersonalityInput onSubmit={handleSubmit} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default Analyze;
