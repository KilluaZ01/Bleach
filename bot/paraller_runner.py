"""Main orchestrator for parallel account creation"""

import multiprocessing
from workflows import run_batch


def run_all_batches(base_instance, total_accounts, instances_per_batch, 
                     guest_name, log_func, pause_event):
    """Run all batches sequentially
    
    Args:
        base_instance: Base name for instances
        total_accounts: Total number of accounts to create
        instances_per_batch: Number of instances per batch
        guest_name: Prefix for guest names
        log_func: Logging function
        pause_event: Threading event for pause control
    """
    total_batches = total_accounts // instances_per_batch
    guest_index = 1

    for batch in range(1, total_batches + 1):
        log_func(f"🚀 Starting batch {batch}")
        run_batch(
            batch, 
            guest_index, 
            instances_per_batch, 
            log_func, 
            base_instance,  
            pause_event
        )
        guest_index += instances_per_batch


if __name__ == "__main__":
    multiprocessing.freeze_support()
    # Example usage
    run_all_batches(
        base_instance="chaos_base",
        total_accounts=10,
        instances_per_batch=2,
        log_func=print,
        pause_event=None
    )