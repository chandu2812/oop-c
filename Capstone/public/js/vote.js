async function castVote() {
    const vId = localStorage.getItem('voterId');
    if (!vId) {
        alert('Session missing. Please log in again.');
        window.location.href = '/';
        return;
    }

    const cId = document.getElementById('candidateSelect').value;
    const res = await fetch('/api/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voter_id: vId, candidate_id: cId })
    });

    if (res.ok) {
        alert('Vote cast successfully.');
    } else {
        alert('Vote rejected. You have already voted.');
    }
}

function logout() {
    localStorage.removeItem('voterId');
    window.location.href = '/';
}