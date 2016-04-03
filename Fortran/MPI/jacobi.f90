program jacobi
    use mpi
    implicit none

    integer, parameter :: Nx  = 240
    integer, parameter :: tag = 0
    integer            :: N, i
    integer            :: ierr, my_mpi_rank, my_mpi_size
    integer            :: recv_request_left, recv_request_right
    real               :: tol, local_err, global_err

    real, allocatable, dimension(:,:,:) :: U


    ! Initialise MPI
    print*, 'Initialising MPI'
    call MPI_INIT(ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_mpi_rank, ierr)
    print*, 'Rank: ', my_mpi_rank
    call MPI_COMM_SIZE(MPI_COMM_WORLD, my_mpi_size, ierr)

    ! Divide array into parallel sections
    N = int(Nx / my_mpi_size)
    print*, 'Rank: ', my_mpi_rank, 'allocating: ', Nx+2, N+2, 2
    ! allocate space for ghost cells
    allocate(U(Nx+2, N+2, 2))

    ! Set initial values, 0 along edges, 1 elsewhere
    ! Set all elements to 1
    U = 1.0
    ! Set edge elements to 0, first short edges
    U(1,    :, 1) = 0.0
    U(Nx+2, :, 1) = 0.0
    ! then long edges on the two ends
    ! Note that MPI uses 0 indexing
    if (my_mpi_rank == 0) then
        U(:, 1,   1) = 0.0
    else if (my_mpi_rank == my_mpi_size - 1) then
        U(:, N+2, 1) = 0.0
    endif

    ! Loop over matrix

    print*, 'Rank: ', my_mpi_rank, 'Entering loop...'
    i = 0
    tol = 1e-9
    global_err = 2*tol
    do while (global_err > tol)
        i = i + 1
        ! Calculate next step, then copy:
        ! next -> current
        U(2:Nx+1, 2:N+1, 2) = ( &
              U(3:,     2:N+1,  1) + U(:Nx,    2:N+1, 1) &
            + U(2:Nx+1, 3:,     1) + U(2:Nx+1, :N,    1) &
            )/4

        ! Calculate error:
        local_err = sum((U(2:Nx+1, 2:N+1, 1) - U(2:Nx+1, 2:N+1, 2))**2)
        call MPI_ALLREDUCE(local_err, global_err, 1, MPI_REAL, MPI_SUM, MPI_COMM_WORLD, ierr)

        ! Print from one process only:
        if (my_mpi_rank == 0) then
            if (mod(i, 1000) == 0) then
                print*, 'Global error: ', global_err
            endif
        endif

        ! Copy (after calculating error)
        U(2:Nx+1, 2:N+1, 1) = U(2:Nx+1, 2:N+1, 2)

        ! Transfer ghost cells
        ! Here we send from U(:,:,2)
        ! and receive into U(:,:,1)

        ! Only do communication if more than one rank
        if (my_mpi_size > 1) then
            ! First, set up non-blocking receive
            if (my_mpi_rank == 0) then
                call MPI_IRECV(U(:, N+2, 1), Nx+2, MPI_REAL, my_mpi_rank + 1, &
                    tag, MPI_COMM_WORLD, recv_request_right, ierr)
            else if (my_mpi_rank == my_mpi_size - 1) then
                call MPI_IRECV(U(:, 1, 1), Nx+2, MPI_REAL, my_mpi_rank - 1, &
                    tag, MPI_COMM_WORLD, recv_request_left, ierr)
            else
                call MPI_IRECV(U(:, N+2, 1), Nx+2, MPI_REAL, my_mpi_rank + 1, &
                    tag, MPI_COMM_WORLD, recv_request_right, ierr)
                call MPI_IRECV(U(:, 1, 1), Nx+2, MPI_REAL, my_mpi_rank - 1, &
                    tag, MPI_COMM_WORLD, recv_request_left, ierr)
            endif

            ! Then, set up blocking send
            if (my_mpi_rank == 0) then
                call MPI_SEND(U(:, N+1, 2), Nx+2, MPI_REAL, my_mpi_rank + 1, &
                    tag, MPI_COMM_WORLD, ierr)
            else if (my_mpi_rank == my_mpi_size - 1) then
                call MPI_SEND(U(:, 2, 1), Nx+2, MPI_REAL, my_mpi_rank - 1, &
                    tag, MPI_COMM_WORLD, ierr)
            else
                call MPI_SEND(U(:, N+1, 1), Nx+2, MPI_REAL, my_mpi_rank + 1, &
                    tag, MPI_COMM_WORLD, ierr)
                call MPI_SEND(U(:, 2, 1), Nx+2, MPI_REAL, my_mpi_rank - 1, &
                    tag, MPI_COMM_WORLD, ierr)
            endif

            ! Then add a barrier to make sure all receives are complete
            call MPI_BARRIER(MPI_COMM_WORLD, ierr)
        endif
    enddo


    print*, 'Rank: ', my_mpi_rank, ' Done.'
    deallocate(U)
    call MPI_FINALIZE(ierr)
end program
