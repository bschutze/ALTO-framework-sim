#!/usr/bin/perl -w

use strict;
use warnings;
use List::Util qw/shuffle/;
use Term::ANSIColor;
use Getopt::Long;

my $factor = $ARGV[0];

my $verbose;
my $debug;
my $retries = 100; # number of re-tries
my $maxLoop = 500; # iteration per try


my $optResult = GetOptions( "debug|d"   => \$debug,
                         "verbose|v" => \$verbose,
                      );

my %links;        # two key hashmap of Source -> Destination -> w (for weight) or c (for configured default)
my %constraints;  # five key hashmap of Source -> destination -> operation (lesser, greater, equal) -> Source -> Destination
my %nodes;        # one key hashmap of node names (needed for output only)


$|++;

## parse input graph file
while (my $line = <STDIN>) {
  chomp($line);
  $line =~ s/#.*$//g;
  $line =~ s/^\s+//;
  $line =~ s/\s+$//;
  if ($line =~ /^([A-Z0-9]+)\s*->\s*([A-Z0-9]+)\s*=\s*(\d+)$/) {
    $links{$1}{$2}{c} = $3;
    print STDERR "Added $1 -> $2 = $links{$1}{$2}{c}\n" if ($verbose || $debug);
  }

  if ($line =~ /^([A-Z]+)\s*->\s*([A-Z]+)\s*([<=>]+)\s*([A-Z]+)\s*->\s*([A-Z]+)$/) {

    my $s = $1;
    my $d = $2;
    my $op = $3;
    my $cs = $4;
    my $cd = $5;

    print "$s -> $d has a constraint but does not exist\n" if (!exists($links{$s}{$d}));
    print "$cs -> $cd has a constraint but does not exist\n" if (!exists($links{$cs}{$cd}));

    if ($op eq "==") {
      $constraints{$s}{$d}{equal}{$cs}{$cd}++;
      print STDERR "added $s -> $d == $cs -> $cd\n" if ($verbose || $debug);
      $constraints{$cs}{$cd}{equal}{$s}{$d}++;
      print STDERR "added $cs -> $cd == $s -> $d\n" if ($verbose || $debug);
    }

    if ($op eq "<") {
      $constraints{$s}{$d}{smaller}{$cs}{$cd}++;
      print STDERR "added $s -> $d <  $cs -> $cd\n" if ($verbose || $debug);
      $constraints{$cs}{$cd}{greater}{$s}{$d}++;
      print STDERR "added $cs -> $cd >  $s -> $d\n" if ($verbose || $debug);
    }

    if ($op eq ">") {
      $constraints{$s}{$d}{greater}{$cs}{$cd}++;
      print STDERR "added $s -> $d >  $cs -> $cd\n" if ($verbose || $debug);
      $constraints{$cs}{$cd}{smaller}{$s}{$d}++;
      print STDERR "added $cs -> $cd <  $s -> $d\n" if ($verbose || $debug);
    }

  }

  if ($line =~ /^symmetrical$/) {
    print STDERR "adding constraints for symmetrical weights\n" if ($verbose || $debug);
    for my $s (sort keys %links) {
      for my $d (sort keys %{$links{$s}}) {
        $constraints{$s}{$d}{equal}{$d}{$s}++;
        print STDERR "  added $s -> $d == $d -> $s\n" if ($debug);
      }
    }
  }
}

#output warnings for unidirectional links
for my $s (sort keys %links) {
  for my $d (sort keys %{$links{$s}}) {
    print STDERR "missing link from $d to $s\n" if (!exists($links{$d}{$s}));
  }
}

#remember all the node names
for my $n (keys %links) {
  $nodes{$n}++ for (keys $links{$n});
}

#try to find a solutions that is geodetic (shortest path is unique for all node combinations)
#  and that meets all the defined constraints
#  Start with the given weights and successively randomize the starting weights as the retires increase
my $result = -1;
my $loop = 0;
while (($retries > $loop) && ($result != 0)) {

  #reset the weights to the initial config + a randomized component
  for my $s(keys %links) {
    for my $d (keys%{$links{$s}}) {
      $links{$s}{$d}{w} = $links{$s}{$d}{c} + int(rand($loop * $factor));
      delete $links{$s}{$d}{f};
    }
  }

  # see if we this configuration solves all the constraints.
  #  this returns zero only if
  #    a) all shortest path are unique and
  #    b) all constraints are met
  $result = makeUnique();
  print STDERR "+";
  $loop++;
}

print STDERR "\n";
($result == 0) ? printResult() : print "could not find solutions.\n";

##print out the final configuration of links
sub printResult {
  print "\n";
  my %path;
  $path{$_} = getPath($_) for (sort keys %nodes);

  my %pathPerLink;
  for my $s (sort keys %path) {
    for my $d (sort keys %{$path{$s}}) {
      for my $p (keys %{$path{$s}{$d}{path}}) {
        my @links = split(/,/,$p);
        for (0 .. scalar(@links)-2) {
          $pathPerLink{$links[$_]}{$links[$_+1]}{t}++;
          $pathPerLink{$links[$_]}{$links[$_+1]}{d}++ if (scalar(keys(%{$path{$s}{$d}{path}})) > 1);
        }
      }
    }
  }

  for my $s (sort keys %links) {
    for my $d (sort keys %{$links{$s}}) {
      my @cCheck;
      for my $op (keys %{$constraints{$s}{$d}}) {
        for my $cs (keys %{$constraints{$s}{$d}{$op}}) {
          for my $cd (keys %{$constraints{$s}{$d}{$op}{$cs}}) {
            my $color = 'red';

            if ($op eq "equal") {
              $color = 'green' if ($links{$s}{$d}{w} == $links{$cs}{$cd}{w});
              push @cCheck, sprintf ("== %s->%s (%s)", $cs, $cd, colored("$links{$s}{$d}{w} == $links{$cs}{$cd}{w}", $color));
            }

            if ($op eq "smaller") {
              $color = 'green' if ($links{$s}{$d}{w} < $links{$cs}{$cd}{w});
              push @cCheck, sprintf ("<  %s->%s (%s)", $cs, $cd, colored("$links{$s}{$d}{w} < $links{$cs}{$cd}{w}", $color));
            }

            if ($op eq "greater") {
              $color = 'green' if ($links{$s}{$d}{w} > $links{$cs}{$cd}{w});
              push @cCheck, sprintf (">  %s->%s (%s)", $cs, $cd, colored("$links{$s}{$d}{w} > $links{$cs}{$cd}{w}", $color));
            }

          }
        }
      }
      printf "%s -> %s = %3i #load: %s(%s) contraints: %s\n",
            $s,
            $d,
            $links{$s}{$d}{w},
            exists($pathPerLink{$s}{$d}{t}) ? colored("$pathPerLink{$s}{$d}{t}", 'green') : colored("0", 'red'),
            exists($pathPerLink{$s}{$d}{d}) ? colored("$pathPerLink{$s}{$d}{d}", 'red') : colored("0", 'green'),
            join(',',@cCheck);
    }
  }
}

# try to turn the current configuration into a geodetic graph that meets all configured constraints
#  this is an iterative heuristic that might not always work...
sub makeUnique {
  my $max = -1;
  my $min = 1;
  my $loop = 0;

  # no dup path and all direct links used !
  while ($max != 0 || $min == 0) {
    ($max, $min, my $dupPathRef) = getDupPathMaxLinkLoad();

    #print "dup path max = $max, min = $min\n";# if ($debug);

    if ($max > 0){
      (my $s) = shuffle keys %{$dupPathRef};
      (my $d) = shuffle keys %{$dupPathRef->{$s}};

      $links{$s}{$d}{w}++;
      print "increase $s -> $d to $links{$s}{$d}{w}\n" if ($debug);

      if (exists($constraints{$s}{$d})) {
        for my $op (keys %{$constraints{$s}{$d}}) {
          for my $cs (keys %{$constraints{$s}{$d}{$op}}) {
            for my $cd (keys %{$constraints{$s}{$d}{$op}{$cs}}) {

              if ($op eq "equal") {
                $links{$cs}{$cd}{w} = $links{$s}{$d}{w};
                print "$s->$d == $cs->$cd ($links{$s}{$d} == $links{$cs}{$cd})\n" if ($debug);
              }

              if ($op eq "smaller") {
                $links{$cs}{$cd}{w} = $links{$s}{$d}{w} + 1 if ($links{$s}{$d}{w} >= $links{$cs}{$cd}{w});
                print "$s->$d < $cs->$cd ($links{$s}{$d} < $links{$cs}{$cd})\n" if ($debug);
              }

              if ($op eq "greater") {
                $links{$cs}{$cd}{w} = $links{$s}{$d}{w} - 1 if ($links{$s}{$d}{w} <= $links{$cs}{$cd}{w});
                print "$s->$d > $cs->$cd ($links{$s}{$d} > $links{$cs}{$cd})\n" if ($debug);
              }
            }
          }
        }
      }



      print STDERR "." if ($loop % 10 == 0);
    } else {
      $max = checkConstraints();
      print STDERR ",";
    }
    $loop++;
    return -1 if ($loop > $maxLoop);
    #print "final result of dup check = $max\n";
  }
  #print "we are done with finding a solution - now try to reduce the weights\n";
  # and now try to reduce the link weights as much as possible
  my $changes = 0;
  while ($changes > 0) {
    $changes = 0;
    for my $s (keys %links) {
      for my $d (keys %{$links{$s}}) {
        my $max = 0;
        while (($max == 0) && ($links{$s}{$d}{w} > 0)){
          $links{$s}{$d}{w}--;
          $max = getDupPathMaxLinkLoad();
        }

        if (($max > 0) || ($links{$s}{$d}{w} == 0)) {
          $changes--;
          $links{$s}{$d}{w}++
        }
        print STDERR "-";
      }
    }
  }
  return 0;
}

# find all non-unique shortest path and map the to links. returns the list of all links that have the highest count
#  of non-unique shortest path crossing them.
sub getDupPathMaxLinkLoad {
  my %path;
  $path{$_} = getPath($_) for (sort keys %nodes);
  my %result;

  my %pathPerLink;
  for my $s (sort keys %path) {
    for my $d (sort keys %{$path{$s}}) {
      for my $p (keys %{$path{$s}{$d}{path}}) {
        my @links = split(/,/,$p);
        for (0 .. scalar(@links)-2) {
          $pathPerLink{$links[$_]}{$links[$_+1]}{t}++;
          $pathPerLink{$links[$_]}{$links[$_+1]}{d}++ if (scalar(keys(%{$path{$s}{$d}{path}})) > 1);
        }
      }
    }
  }

  my $max = 0;
  my $min;
  for my $s (sort keys %links) {
    for my $d (sort keys %{$links{$s}}) {
   #   print "Link $s -> $d = $links{$s}{$d} ".(exists($pathPerLink{$s}{$d}) ? $pathPerLink{$s}{$d} : 0)."\n";

      if (exists($pathPerLink{$s}{$d}{d}) && ($pathPerLink{$s}{$d}{d} >= $max)) {
        if ($pathPerLink{$s}{$d}{d} >= $max) {
          $max = $pathPerLink{$s}{$d}{d};
          delete $result{$_} for keys %result;
        }
        $result{$s}{$d}++;
      }
      if (exists($pathPerLink{$s}{$d}{t})) {
        $min = $pathPerLink{$s}{$d}{t} if (!defined($min) || ($min > $pathPerLink{$s}{$d}{t}));
      } else {
        $min = 0;
      }
    }
  }
  return $max, $min, \%result;
}

# Checks the con
sub checkConstraints {
  my $errors = 0;
  for my $s (sort keys %links) {
    for my $d (sort keys %{$links{$s}}) {
      for my $op (keys %{$constraints{$s}{$d}}) {
        for my $cs (keys %{$constraints{$s}{$d}{$op}}) {
          for my $cd (keys %{$constraints{$s}{$d}{$op}{$cs}}) {

            if ($op eq "equal") {
              if (!($links{$s}{$d}{w} == $links{$cs}{$cd}{w})) {
                $errors++;
                #print "[C] set $s->$d($links{$s}{$d}{w}) = $cs -> $cd ($links{$cs}{$cd}{w} => $links{$cs}{$cd}{w})\n";
                $links{$cs}{$cd}{w} = $links{$s}{$d}{w};
              }
            }

            if ($op eq "smaller") {
               if (!($links{$s}{$d}{w} < $links{$cs}{$cd}{w})) {
                 $errors++;
                 #print "[C] set $s->$d($links{$s}{$d}{w}) < $cs -> $cd($links{$cs}{$cd}{w} => ".($links{$s}{$d}{w} - 1).")\n";
                 $links{$cs}{$cd}{w} = $links{$s}{$d}{w} + 2;#int(rand($links{$s}{$d}{w}-1)) + 1;
               }
            }

            if ($op eq "greater") {
              if (!($links{$s}{$d}{w} > $links{$cs}{$cd}{w})) {
                $errors++;
                #print "[C] set $s->$d ($links{$s}{$d}{w}) > $cs -> $cd ($links{$cs}{$cd}{w} => ".($links{$s}{$d}{w} + 2).")\n";
                $links{$cs}{$cd}{w} = $links{$s}{$d}{w} - 1;#int(rand($links{$s}{$d}{w}));

              }
            }

          }
        }
      }
    }
  }

  return $errors;
}

sub getPath {
  (my $start, my $print) = @_;

  my %visited;
  $visited{$start}{dist} = 0;

  my %neighbors;
  $neighbors{$_}{dist} = $links{$start}{$_}{w} for (keys %{$links{$start}});
  $neighbors{$_}{path}{$start}++ for (keys $links{$start});

  while (scalar(keys(%neighbors)) > 0) {

    (my $next) = sort {$neighbors{$a}{dist} <=> $neighbors{$b}{dist}} (keys %neighbors);
    my $nextDist = $neighbors{$next}{dist};

    if ($print) {
      print "  select $next=$nextDist\n";
      print "    visited   ".(join(',', map("$_=$visited{$_}{dist}(".(join('+',sort keys %{$visited{$_}{path}})).")", sort keys %visited)))."\n";
      print "    neighbors ".(join(',', map("$_=$neighbors{$_}{dist}(".(join('+',sort keys %{$neighbors{$_}{path}})).")", sort keys %neighbors)))."\n";
    }

    $visited{$next}{dist} = $nextDist;
    $visited{$next}{path}{$_}++ for (keys %{$neighbors{$next}{path}});

    delete $neighbors{$next};

    for my $n (keys %{$links{$next}}) {
       # check that this one is not finished yet
       if (!exists($visited{$n})) {

         # check that we have not found it before
         if (!exists($visited{$n})) {
           if (!exists($neighbors{$n})) {
             $neighbors{$n}{dist} = $links{$next}{$n}{w} + $nextDist;

             $neighbors{$n}{path}{"$_,$next"}++ for keys %{$visited{$next}{path}};

           } else {
             if ($links{$next}{$n}{w} + $nextDist <= $neighbors{$n}{dist}) {
               if ($links{$next}{$n}{w} + $nextDist < $neighbors{$n}{dist}) {
                 $neighbors{$n}{dist} = $links{$next}{$n}{w} + $nextDist;
                 delete $neighbors{$n}{path};
               }
               $neighbors{$n}{path}{"$_,$next"}++ for keys %{$visited{$next}{path}};
               #$neighbors{$n}{path}{$next}++;
             }
           }
         }
       }
    }
    #sleep 1;
  }

  for my $v (sort keys %visited) {
    for my $p (keys %{$visited{$v}{path}}) {
      $visited{$v}{path}{"$p,$v"}++;
      delete $visited{$v}{path}{$p};
    }
  }

  return \%visited;
}
