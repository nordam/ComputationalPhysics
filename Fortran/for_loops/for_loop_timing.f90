program loop_example

    ! Parameter defining double precision
    integer, parameter :: DP = kind(1.0D0)

    ! Matrix size
    integer, parameter :: N = 5000000

    integer :: i

    real(DP), dimension(N)    :: a, b, c

    ! Variables for keeping track of time
    real(DP) :: tic, toc

    ! Fill a and b with random numbers
    call random_number(a)
    call random_number(b)

    ! Element-wise multiplication with for loop
    call cpu_time(tic)
    do i = 1, N
        c(i) = a(i) * b(i)
    end do
    call cpu_time(toc)
    print*, 'For loop took ', toc - tic, ' seconds, info = ', info

    ! Element-wise multiplication without for loop
    call cpu_time(tic)
    c = a * b
    call cpu_time(toc)
    print*, 'Without for loop took ', toc - tic, ' seconds, info = ', info


end program loop_example
