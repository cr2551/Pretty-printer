;;;apply
(begin (set! car b*) (define (sq x) (car x x)) (apply sq '(3)))
