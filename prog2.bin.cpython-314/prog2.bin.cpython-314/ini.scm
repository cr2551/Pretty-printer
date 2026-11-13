(define (eqv? x y)
  (if (and (number? x) (number? y)) (b= x y)
      (eq? x y)))

; doesn't recurse down both car and cdr
; doesn't work for (equal? '(1 (2 3) 4) (list 1 '(2 3) 4))
(define (equal? x y)
  (cond ((null? x) (null? y))
	((null? y) #f)
	((eqv? (car x) (car y)) (equal? (cdr x) (cdr y)))
	(else #f)))

(define (b> x y) (b< y x))
(define (b<= x y) (or (b= x y) (b< x y)))
(define (b>= x y) (or (b= x y) (b> x y)))

(define (= x y . l)
  (if (null? l) (b= x y)
      (and (b= x y) (apply = (cons y l)))))

(define (< x y . l)
  (if (null? l) (b< x y)
      (and (b< x y) (apply < (cons y l)))))

(define (> x y . l)
  (if (null? l) (b> x y)
      (and (b> x y) (apply > (cons y l)))))

(define (<= x y . l)
  (if (null? l) (b<= x y)
      (and (b<= x y) (apply <= (cons y l)))))

(define (>= x y . l)
  (if (null? l) (b>= x y)
      (and (b>= x y) (apply >= (cons y l)))))

(define (zero? x) (b= x 0))
(define (positive? x) (b< 0 x))
(define (negative? x) (b< x 0))

(define (odd? x) "not yet implemented")
(define (even? x) "not yet implemented")

(define (max . l) "not yet implemented")
(define (min . l) "not yet implemented")

(define (+ . l)
  (if (null? l) 0
      (b+ (car l) (apply + (cdr l)))))

; - is not implemented correctly
(define (- . l)
  (if (null? l) 0
      (b- (car l) (apply - (cdr l)))))

(define (* . l)
  (if (null? l) 1
      (b* (car l) (apply * (cdr l)))))

(define (not b) (if b #f #t))
(define (and x y) (if x y #f))
(define (or x y) (if x #t y))

(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))
(define (caaar x) (car (car (car x))))
(define (caadr x) (car (car (cdr x))))
(define (cadar x) (car (cdr (car x))))
(define (caddr x) (car (cdr (cdr x))))
(define (cdaar x) (cdr (car (car x))))
(define (cdadr x) (cdr (car (cdr x))))
(define (cddar x) (cdr (cdr (car x))))
(define (cdddr x) (cdr (cdr (cdr x))))
(define (caaaar x) (car (car (car (car x)))))
(define (caaadr x) (car (car (car (cdr x)))))
(define (caadar x) (car (car (cdr (car x)))))
(define (caaddr x) (car (car (cdr (cdr x)))))
(define (cadaar x) (car (cdr (car (car x)))))
(define (cadadr x) (car (cdr (car (cdr x)))))
(define (caddar x) (car (cdr (cdr (car x)))))
(define (cadddr x) (car (cdr (cdr (cdr x)))))
(define (cdaaar x) (cdr (car (car (car x)))))
(define (cdaadr x) (cdr (car (car (cdr x)))))
(define (cdadar x) (cdr (car (cdr (car x)))))
(define (cdaddr x) (cdr (car (cdr (cdr x)))))
(define (cddaar x) (cdr (cdr (car (car x)))))
(define (cddadr x) (cdr (cdr (car (cdr x)))))
(define (cdddar x) (cdr (cdr (cdr (car x)))))
(define (cddddr x) (cdr (cdr (cdr (cdr x)))))

(define (list . l) l)

(define (length l)
  (if (null? l) 0
      (b+ 1 (length (cdr l)))))

(define (append . l)
  (define (app x y)
    (if (null? x) y
	(cons (car x) (app (cdr x) y))))
  (if (null? l) '()
      (app (car l) (apply append (cdr l)))))

(define (reverse l)
  (define (rev l r)
    (if (null? l) r
	(rev (cdr l) (cons (car l) r))))
  (rev l '()))

(define (memq e l)
  (cond ((null? l) #f)
	((eq? e (car l)) l)
	(else (memq e (cdr l)))))

(define (memv e l)
  (cond ((null? l) #f)
	((eqv? e (car l)) l)
	(else (memv e (cdr l)))))

(define (member e l)
  (cond ((null? l) #f)
	((equal? e (car l)) l)
	(else (member e (cdr l)))))

; (assq 'x ((x 3) (y 4))) (with missing quote) causes endless loop
(define (assq e l)
  (cond ((null? l) #f)
	((eq? e (caar l)) (car l))
	(else (assq e (cdr l)))))

(define (assv e l)
  (cond ((null? l) #f)
	((eqv? e (caar l)) (car l))
	(else (assv e (cdr l)))))

(define (assoc e l)
  (cond ((null? l) #f)
	((equal? e (caar l)) (car l))
	(else (assoc e (cdr l)))))

; n-ary map not yet implemented
(define (map f l)
  (if (null? l) '()
      (cons (f (car l)) (map f (cdr l)))))

; n-ary for-each not yet implemented
(define (for-each f l)
  (if (null? l) '()
      (begin (f (car l)) (for-each f (cdr l)))))

(define (eof-object? x)
  (eq? x 'end-of-file))
