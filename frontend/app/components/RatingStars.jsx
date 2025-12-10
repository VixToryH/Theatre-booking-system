"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function RatingStars({ showId }) {
    const [rating, setRating] = useState(0);
    const [hover, setHover] = useState(0);

    useEffect(() => {
    api.get(`/api/mlrate/rate/${showId}/`)
        .then(res => {
            setRating(res.data.rating);
        })
        .catch(() => {});
}, [showId]);

        
    const handleRate = (value) => {
        api.post("/api/mlrate/rate/", {
            show_id: showId,
            rating: value
        })
        .then(res => {
            setRating(value);
        })
        .catch(err => {
            if (err.response?.status === 401) {
                alert("Спочатку увійдіть в акаунт!");
            }
        });
    };

    return (
        <div style={{ 
            display: "flex",
    gap: "5px",
    fontSize: "32px",
    justifyContent: "center",
    width: "100%",
    position: "relative",
    zIndex: 999999,    
    pointerEvents: "auto" 
            }}>
            {[1, 2, 3, 4, 5].map((star) => (
                <span
                    key={star}
                    onClick={() => handleRate(star)}
                    
                    onMouseEnter={() => setHover(star)}
                    onMouseLeave={() => setHover(0)}
                    style={{
                        cursor: "pointer",
                        color:
                            star <= (hover || rating) ? "#FFD700" : "#ccc"
                    }}
                >
                    ★
                </span>
            ))}
        </div>
    );
}
