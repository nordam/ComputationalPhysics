program diffusion
    implicit none

    real    :: T, dt, dx, alpha
    integer :: Nt, Nx, i, it
    real, allocatable, dimension(:,:) :: U

    Nx = 8000
    ! Simulating over a range from x = -5 to x = 5
    dx = 10.0/(Nx-1)

    T  = 0.1
    ! Calculate dt according to stability criterion
    ! (in this example, D = 1)
    dt = 0.5*dx**2
    Nt = T/dt

    alpha = dt/dx**2
    !print*, 'alpha = ', alpha

    allocate(U(Nx+2, Nt))
    ! Initial conditions
    U = 0
    U(Nx/4:3*Nx/4, 1) = 1

    do it = 2, Nt
        !$OMP PARALLEL DO
        do i = 2, Nx+1
            U(i, it) = U(i, it-1) + alpha*(U(i+1, it-1) - 2*U(i, it-1) + U(i-1, it-1))
        end do
        !$OMP END PARALLEL DO
    end do

    print*, U(:,Nt)
    deallocate(U)
end program
