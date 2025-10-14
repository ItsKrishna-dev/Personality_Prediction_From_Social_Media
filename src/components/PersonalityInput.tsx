import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus, X, Sparkles } from "lucide-react";
import { toast } from "sonner";

interface PersonalityInputProps {
  onSubmit: (comments: string[]) => void;
  isLoading: boolean;
}

export const PersonalityInput = ({ onSubmit, isLoading }: PersonalityInputProps) => {
  const [comments, setComments] = useState<string[]>([""]);

  const addComment = () => {
    if (comments.length < 10) {
      setComments([...comments, ""]);
    } else {
      toast.error("Maximum 10 comments allowed");
    }
  };

  const removeComment = (index: number) => {
    if (comments.length > 1) {
      setComments(comments.filter((_, i) => i !== index));
    }
  };

  const updateComment = (index: number, value: string) => {
    const newComments = [...comments];
    newComments[index] = value;
    setComments(newComments);
  };

  const handleSubmit = () => {
    const validComments = comments.filter(c => c.trim().length > 0);
    
    if (validComments.length === 0) {
      toast.error("Please enter at least one comment");
      return;
    }

    if (validComments.some(c => c.length < 10)) {
      toast.error("Each comment should be at least 10 characters");
      return;
    }

    onSubmit(validComments);
  };

  return (
    <Card className="w-full max-w-3xl shadow-card border-border/50 backdrop-blur-sm bg-card/80">
      <CardHeader className="space-y-2">
        <div className="flex items-center gap-2">
          <Sparkles className="h-6 w-6 text-primary" />
          <CardTitle className="text-3xl text-gradient">Discover Your Personality</CardTitle>
        </div>
        <CardDescription className="text-base">
          Share your thoughts, experiences, or opinions in the text areas below. 
          The more you write, the more accurate your personality analysis will be.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {comments.map((comment, index) => (
          <div key={index} className="relative group">
            <Textarea
              value={comment}
              onChange={(e) => updateComment(index, e.target.value)}
              placeholder={`Comment ${index + 1}: Share your thoughts, experiences, or opinions...`}
              className="min-h-[100px] resize-none transition-all focus:shadow-glow"
              disabled={isLoading}
            />
            {comments.length > 1 && (
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                onClick={() => removeComment(index)}
                disabled={isLoading}
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
        ))}

        <div className="flex gap-3 pt-2">
          {comments.length < 10 && (
            <Button
              type="button"
              variant="outline"
              onClick={addComment}
              disabled={isLoading}
              className="flex-1"
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Another Comment
            </Button>
          )}
          
          <Button
            onClick={handleSubmit}
            disabled={isLoading}
            className="flex-1 bg-gradient-to-r from-primary to-primary-glow hover:opacity-90 transition-opacity shadow-glow"
          >
            {isLoading ? (
              <>
                <div className="h-4 w-4 mr-2 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 mr-2" />
                Analyze Personality
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
