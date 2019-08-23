class Vm:
    def __init__(self, umax: int, ttask: int, users: int):
        """
        :param umax: max user per vm
        :param ttask: Number of ticks
        :param users: number of users
        """
        self.umax = umax
        self.ttask = ttask
        if umax < users:
            raise Exception('Number of users exceed umax')
        self.users = [ttask for _ in range(users)]
        self.total_users = users

    def insert_user(self, new_users: int):
        """
        Insert users on this VM

        :param new_users:
        :return: number of users inserted in this VM
        """
        if self.total_users == self.umax:
            return 0

        elif new_users + self.total_users <= self.umax:
            self.users += [self.ttask for _ in range(new_users)]
            self.total_users += new_users
            return new_users

        else:
            users_to_insert = self.umax - self.total_users
            self.users += [self.ttask for _ in range(users_to_insert)]
            self.total_users = self.umax
            return users_to_insert

    def tick(self):
        """
        Execute one tick on this VM

        :return: None
        """
        preserv = []
        for i in range(self.total_users):
            self.users[i] -= 1
            if not self.users[i] == 0:
                preserv.append(i)
            else:
                self.total_users -= 1

        self.users = [self.users[i] for i in preserv]



class LoadBalancer:
    def __init__(self, ttask: int, umax: int, vm_cost:int =1):
        self.cluster = []
        self.cluster_size = 0
        self.snapshots = []
        self.total_coast = 0
        self.vm_cost = vm_cost

        if 1 <= ttask <= 10:
            self.ttask = ttask
        else:
            raise Exception("ttask need to be between 1 and 10")

        if 1 <= umax <= 10:
            self.umax = umax
        else:
            raise Exception("umax need to be between 1 and 10")

    def __tick(self):
        """
        Execute one tick on this cluster

        :return: None
        """
        preserv = []
        for i in range(self.cluster_size):
            self.cluster[i].tick()
            if not self.cluster[i].total_users == 0:
                preserv.append(i)
            else:
                self.cluster_size -= 1
        self.cluster = [self.cluster[i] for i in preserv]

    def __balance(self, users: int):
        """
        Allocate users to this cluster, create more VMs if needed

        :param users: Number of users to balance
        :return:
        """
        vm_id = 0
        while users > 0:
            if vm_id < self.cluster_size:
                users -= self.cluster[vm_id].insert_user(new_users=users)
                vm_id += 1
            else:
                if users > self.umax:
                    users -= self.umax
                    self.cluster.append(Vm(self.umax, self.ttask, self.umax))
                    self.cluster_size += 1
                else:
                    self.cluster.append(Vm(self.umax, self.ttask, users))
                    self.cluster_size += 1
                    users -= users

    def __snapshot(self):
        """
        Take a snapshot about cluster configuration on the current tick, calculate costs

        :return: None
        """
        if self.cluster_size > 0:
            self.snapshots.append(','.join(str(vm.total_users) for vm in self.cluster))
            self.total_coast += (self.cluster_size * self.vm_cost)
        else:
            self.snapshots.append('0')

    @property
    def report(self):
        """
        :return: report about all process in cluster, with total costs
        """
        return self.snapshots + [str(self.total_coast)]

    def process(self, tasks: list):
        """
        Main process of this cluster
        :param tasks: process timeline
        :return: None
        """
        task_size = len(tasks)
        if task_size < 0:
            raise Exception("tasks need to be more than 0")

        tick_size = 0
        time_line = 0
        while tick_size >= 0 or time_line < task_size:
            self.__tick()
            if time_line < task_size:
                self.__balance(tasks[time_line])
                if tasks[time_line] > 0:
                    tick_size = self.ttask

            self.__snapshot()
            time_line += 1
            tick_size -= 1



