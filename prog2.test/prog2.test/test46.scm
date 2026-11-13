;;;lambda
(begin
  (define foo
            (let ((x 4))
              (lambda (y) (b+ x y))))
  (foo 6))
