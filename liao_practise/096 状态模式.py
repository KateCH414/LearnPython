# --*-- coding:utf-8 --*--
"""
状态模式
面向对象编程着力于在对象交互时改变它们的状态
在很多问题中，有限状态机（通常名为状态机）是一个非常方便的状态转换建模（并在必要时以数学方式形式化）工具
什么是状态机？状态机是一个抽象机器，有两个关键部分，状态和转换。状态是指系统的当前（激活）状况。
转换是指从一个状态切换到另一个状态，因某个事件或条件的触发而开始。
    通常，在一次转换发生之前或之后会执行一个或一组动作。
状态机的一个不错的特性是可以用图来表现（称为状态图），其中每个状态都是一个节点， 每个转换都是两个节点之间的边。

状态机可用于解决多种不同的问题，包括非计算机的问题
非计算机的例子包括自动售货机、电梯、交通灯、暗码锁、停车计时器、自动加油泵及自然语言文法描述
计算机方面的例子包括游戏编程和计算机编程的其他领域、硬件设计、协议设计， 以及编程语言解析。

状态机如何关联到状态设计模式（State design pattern）呢？其实状态模式就是应用到一个特定软件工程问题的状态机。
"""

"""
状态机编译器（State Machine Compiler，SMC）
使用 SMC，你可以使用一种简单的领域特定语言在文本文件中描述你的状态机，SMC 会自动生成状态机的代码。
该项目声称这种 DSL 非常简单，写起来就像一对一地翻译一个状态图。
SMC 可以生成多种编程语言的代码，包括 Python。
"""

"""
状态模式适用于许多问题。所有可以使用状态机解决的问题都是不错的状态模式应用案例。
已经见过的一个例子是操作系统/嵌入式系统的进程模型。
编程语言的编译器实现是另一个好例子。词法和句法分析可使用状态来构建抽象语法树。
事件驱动系统也是另一个例子。在一个事件驱动系统中，从一个状态转换到另一个状态会触发一个事件/消息。许多计算机游戏都使用这一技术。
"""

"""
基于状态图创建一个状态机
状态机应该覆盖一个进程的不同状态以及它们之间的转换。

状态设计模式通常使用一个父 State 类和许多派生的 ConcreteState 类来实现，
父类包含所有状态共同的功能，每个派生类则仅包含特定状态要求的功能。

使用 state_machine 模块创建状态机的第一个步骤是使用 @acts_as_state_machine 修饰器。
在 state_machine 模块中，一个状态转换就是一个 Event。
state_machine 模块提供 @before 和 @after 修饰器，用于在状态转换之前或之后执行动作。
注意如何使用 stat_machine 这样的一个好模块来消除条件式逻辑。
没有必要使用冗长易错的 if-else 语句来检测每个状态转换并作出反应。
"""
from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition

# 状态机
@acts_as_state_machine
class Process:
    # 定义各种状态
    created = State(initial=True)  # 指定状态机的初始状态
    waiting = State()
    running = State()
    terminated = State()  #
    blocked = State()
    swapped_out_waiting = State()
    swapped_out_blocked = State()

    # 定义状态转换，每个转换都是一个 Event，使用 from_states 和 to_state 来定义一个可能的转换
    wait = Event(from_states=(created, running, blocked,
                              swapped_out_waiting), to_state=waiting)

    run = Event(from_states=waiting, to_state=running)

    terminate = Event(from_states=running, to_state=terminated)

    block = Event(from_states=(running, swapped_out_blocked),
                  to_state=blocked)

    swap_wait = Event(from_states=waiting, to_state=swapped_out_waiting)

    swap_block = Event(from_states=blocked, to_state=swapped_out_blocked)

    # 进程独有的信息，比如名称
    def __init__(self, name):
        self.name = name

    # 用于在转换之前或之后执行动作
    @after('wait')
    def wait_info(self):
        print('{} entered waiting mode'.format(self.name))

    @after('run')
    def run_info(self):
        print('{} is running'.format(self.name))

    @before('terminate')
    def terminate_info(self):
        print('{} terminated'.format(self.name))

    @after('block')
    def block_info(self):
        print('{} is blocked'.format(self.name))

    @after('swap_wait')
    def swap_wait_info(self):
        print('{} is swapped out and waiting'.format(self.name))

    @after('swap_block')
    def swap_block_info(self):
        print('{} is swapped out and blocked'.format(self.name))


# 分别是 Process 实例、Event 实例、事件的名称
def transition(process, event, event_name):
    try:
        event()
    except InvalidStateTransition as err:
        print("Error: transition of {} from {} to {} failed".format(process.name,
                                                                    process.current_state, event_name))

# 展示进程当前(激活)状态的一些基本信息
def state_info(process):
    print('state of {}: {}'.format(process.name, process.current_state))

def main():
    RUNNING = 'running'
    WAITING = 'waiting'
    BLOCKED = 'blocked'
    TERMINATED = 'terminated'

    p1, p2 = Process('process1'), Process('process2')

    [state_info(p) for p in (p1, p2)]

    # 不断进行状态转换
    print()
    transition(p1, p1.wait, WAITING)
    transition(p2, p2.terminate, TERMINATED)
    [state_info(p) for p in (p1, p2)]

    print()
    transition(p1, p1.run, RUNNING)
    transition(p2, p2.wait, WAITING)
    [state_info(p) for p in (p1, p2)]

    print()
    transition(p2, p2.run, RUNNING)
    [state_info(p) for p in (p1, p2)]

    print()
    [transition(p, p.block, BLOCKED) for p in (p1, p2)]
    [state_info(p) for p in (p1, p2)]

    print()
    [transition(p, p.terminate, TERMINATED) for p in (p1, p2)]
    [state_info(p) for p in (p1, p2)]


if __name__ == '__main__':
    main()



