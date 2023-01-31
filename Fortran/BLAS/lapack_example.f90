program lapack_example

    ! Parameter defining double precision
    integer, parameter :: DP = kind(1.0D0)

    ! Matrix size
    integer, parameter :: N = 5000

    ! System matrix
    real(DP), dimension(N, N) :: A, A_copy
    ! Right-hand side and solution vector
    real(DP), dimension(N)    :: b, b_copy, x

    ! work matrix needed by the lapack solver
    integer, dimension(N, N)  :: ipiv
    integer :: info

    ! Variables for keeping track of time
    real(DP) :: tic, toc

    ! Fill A and x with random numbers
    call random_number(A)
    call random_number(x)
    ! Compute b with dgemv (Double precision GEneral Matrix-Vector product)
    call dgemv('N', N, N, 1.0_DP, A, N, x, 1, 0.0_DP, b, 1)

    ! Make copies of A and B, as these will be overwritten by the solver
    A_copy = A
    b_copy = b
    ! set x to zero
    x = 0

    ! Solve with dgesv
    call cpu_time(tic)
    ! Note: dgesv overwrites A and b
    ! On input, A is the system matrix, and b is the right-hand side
    ! On output, A is the LU-decomposition (together with ipiv), and b is the solution
    call dgesv(N, 1, A, N, ipiv, b, N, info)
    call cpu_time(toc)
    print*, 'Lapack solver took ', toc - tic, ' seconds, info = ', info

    ! copy solution across to x
    x = b

    ! Confirm that x solves the equation by computing b = Ax, and comparing b and b_copy
    call dgemv('N', N, N, 1.0_DP, A_copy, N, x, 1, 0.0_DP, b, 1)
    print*, 'Largest difference between b and b_copy:', maxval(abs(b - b_copy))

end program lapack_example
