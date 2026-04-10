from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_nutrition_plan(user_profile, total_days=7, chunk_size=2):
    results = {}

    def process_chunk(start_day):
        prompt = build_nutrition_prompt(
            user_profile,
            start_day=start_day,
            num_days=chunk_size
        )

        return invoke_with_retry(llm, prompt)

    start_days = list(range(1, total_days + 1, chunk_size))

    # 🔥 IMPORTANT: reduce workers
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_chunk, day) for day in start_days]

        for future in as_completed(futures):
            try:
                result = future.result()
                results.update(result)
            except Exception as e:
                logger.error(f"Chunk failed: {e}")

    return results