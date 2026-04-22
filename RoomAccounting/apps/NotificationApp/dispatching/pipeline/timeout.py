from concurrent.futures import ThreadPoolExecutor


def execute_with_timeout(sender_class, identifier, canonical_message, timeout_seconds):
    
    if timeout_seconds is not None:
                        
        with ThreadPoolExecutor(max_workers=1) as executor:
            
            future = executor.submit(
                sender_class.send,
                identifier=identifier,
                message=canonical_message,
            )
            future.result(timeout=timeout_seconds)
            
    else:
        sender_class.send(
            identifier=identifier,
            message=canonical_message,
        )
