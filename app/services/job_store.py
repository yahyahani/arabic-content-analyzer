"""
In-memory opslag van jobs.
Voor V1 is dit voldoende; later kun je dit vervangen door Redis
of een database als je meerdere servers/workers wilt draaien.
"""
from app.models.schemas import Job, JobStatus
from threading import Lock

_jobs: dict[str, Job] = {}
_lock = Lock()


def create_job(job_id: str, youtube_url: str) -> Job:
    job = Job(job_id=job_id, youtube_url=youtube_url)
    with _lock:
        _jobs[job_id] = job
    return job


def get_job(job_id: str) -> Job | None:
    with _lock:
        return _jobs.get(job_id)


def update_job(job_id: str, **fields) -> None:
    with _lock:
        job = _jobs.get(job_id)
        if job is None:
            return
        for key, value in fields.items():
            setattr(job, key, value)
        _jobs[job_id] = job
