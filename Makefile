PROG =		arecord
SRC =		arecord.c

PREFIX ?=	/usr/local
BINDIR ?=	${PREFIX}/bin
MAN1DIR ?=	${PREFIX}/man/man1

CC ?=		gcc
CFLAGS ?=	-O2 -pipe
CFLAGS +=	-Wall -ffast-math -fsigned-char

INSTALL =	install

INCLUDEFLAGS ?=	-I${PREFIX}/include
LINKFLAGS ?=	-L${PREFIX}/lib
LINKFLAGS +=    -lasound

all: ${PROG}

${PROG}: ${SRC}
	${CC} ${CFLAGS} ${PTHREADFLAGS} ${INCLUDEFLAGS} ${LINKFLAGS} -o ${PROG} $<

install: ${PROG}
	${INSTALL} -c -m 555 -o root -g bin ${PROG} ${BINDIR}

clean:
	-@rm -f ${PROG} *~ core *.core
