from app.models import CreditTransaction, CreditTransactionType, GenerationJob, User


def estimate_credits(text: str) -> int:
  return max(1, (len(text.strip()) + 99) // 100)


def reserve_credits(user: User, job: GenerationJob, amount: int) -> CreditTransaction:
  if user.credit_balance < amount:
    raise ValueError("Not enough credits")

  user.credit_balance -= amount
  job.reserved_credits = amount
  return CreditTransaction(
    user_id=user.id,
    amount=-amount,
    type=CreditTransactionType.reserve,
    reason="tts_generation_reserved",
    job_id=job.id,
  )


def refund_credits(user: User, job: GenerationJob) -> CreditTransaction:
  amount = job.reserved_credits or 0
  user.credit_balance += amount
  return CreditTransaction(
    user_id=user.id,
    amount=amount,
    type=CreditTransactionType.refund,
    reason="tts_generation_failed",
    job_id=job.id,
  )


def consume_credits(job: GenerationJob) -> CreditTransaction:
  used = job.reserved_credits or 0
  job.used_credits = used
  return CreditTransaction(
    user_id=job.user_id,
    amount=0,
    type=CreditTransactionType.consume,
    reason="tts_generation_completed",
    job_id=job.id,
  )

