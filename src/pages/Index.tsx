import { useState } from "react";
import { PersonalityInput } from "@/components/PersonalityInput";
import { PersonalityResults } from "@/components/PersonalityResults";
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

const Index = () => {
  const [results, setResults] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

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
        setResults(data);
        toast.success("Personality analysis complete!");
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

  const handleReset = () => {
    setResults(null);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full flex items-center justify-center">
        {!results ? (
          <PersonalityInput onSubmit={handleSubmit} isLoading={isLoading} />
        ) : (
          <PersonalityResults
            scores={results.scores}
            interpretations={results.interpretations}
            summary={results.summary}
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  );
};

export default Index;
