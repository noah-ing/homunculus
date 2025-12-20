// HOMUNCULUS Personal Visit Tracker
class PersonalStats {
    constructor() {
        this.stats = this.loadStats();
        this.trackVisit();
        this.updateDisplay();
    }
    
    loadStats() {
        const stored = localStorage.getItem('homunculus_personal_stats');
        return stored ? JSON.parse(stored) : {
            myVisits: 0,
            myGamesPlayed: 0,
            myHighScore: 0,
            firstVisit: Date.now()
        };
    }
    
    trackVisit() {
        this.stats.myVisits++;
        this.saveStats();
    }
    
    trackGamePlay() {
        this.stats.myGamesPlayed++;
        this.saveStats();
        this.updateDisplay();
    }
    
    updateHighScore(score) {
        if (score > this.stats.myHighScore) {
            this.stats.myHighScore = score;
            this.saveStats();
            this.updateDisplay();
        }
    }
    
    saveStats() {
        localStorage.setItem('homunculus_personal_stats', JSON.stringify(this.stats));
    }
    
    updateDisplay() {
        const display = document.querySelector('.stats-display');
        if (display) {
            display.innerHTML = `
                <div>🔄 My Visits: ${this.stats.myVisits}</div>
                <div>🎮 Games Played: ${this.stats.myGamesPlayed}</div>
                <div>🏆 My High Score: ${this.stats.myHighScore}</div>
            `;
        }
    }
}

const personalStats = new PersonalStats();
