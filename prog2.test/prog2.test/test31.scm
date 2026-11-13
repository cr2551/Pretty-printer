;;set-car
(begin (define x (cons 'a (cons 'b '()))) (set-car! x 'c) x)
