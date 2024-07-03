import {moveBall} from "./Ball.js";
import {setPositionPlayer1} from "./Player-1.js";
import {setPositionPlayer2} from "./Player-2.js";

let ws;
let handleKeyDown;

export function loadWS(url, scores){

    //console.log('Connecting to WS server at ' + url);
    ws = new WebSocket(url);

    ws.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        if (data.ball)
            moveBall(data.ball.x, data.ball.y);
        if (data.paddle_one) {
            setPositionPlayer1(data.paddle_one.x, data.paddle_one.y);
            scores.player1 = data.paddle_one.score;
        }
        if (data.paddle_two) {
            setPositionPlayer2(data.paddle_two.x, data.paddle_two.y);
            scores.player2 = data.paddle_two.score;
        }
        if (data.game_state)
            scores.state = data.game_state;
        if (data.error)
            scores.error = data.error;
        else
            scores.error = '';
    });
}

export function unloadWS() {
    ws.close();
}

export function loadInput(window) {
    handleKeyDown = (event) => {
        switch (event.key) {
            case 'ArrowUp':
                ws.send(JSON.stringify({ direction: 'down' }));
                break;
            case 'ArrowDown':
                ws.send(JSON.stringify({ direction: 'up' }));
                break;
        }
    };

    window.addEventListener('keydown', handleKeyDown);
}

export function unloadInput(window) {
    window.removeEventListener('keydown', handleKeyDown);
}