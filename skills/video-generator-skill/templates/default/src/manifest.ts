import { staticFile } from "remotion";

export const manifest = {
    images: [
        staticFile("assets/futuristic_terminal_AI_coding_1_pexels.png"),
        staticFile("assets/futuristic_terminal_AI_coding_2_pexels.png"),
        staticFile("assets/futuristic_terminal_AI_coding_3_pexels.jpeg"),
        staticFile("assets/futuristic_terminal_AI_coding_4_pexels.jpeg"),
        staticFile("assets/futuristic_terminal_AI_coding_5_pexels.jpeg"),
    ],
    music: staticFile("assets/pop_music.mp3"),
    phrases: [
        "GEMINI CLI",
        "AI POWERED",
        "TERMINAL",
        "CODING",
        "TRY IT NOW"
    ],
    durationPerSlide: 60,
    fps: 30
};
