//
//  ActionStateRowView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/25/23.
//
import SwiftUI

struct ActionStateRowView: View {
    @ObservedObject var vm: ActionStateRowViewModel

    var body: some View {
        
        HStack {
            // EXECUTION //
            if vm.containsQuickActionButtonOne {
                Button(
                    action:{
                        vm.handleQuickActionButtonOnePressed()
                    },
                    label: {
                        HStack {
                            Image(systemName: "play.circle.fill")
                                .font(.largeTitle)
                        }
                    })
                .buttonStyle(.plain)
            }
            
            // EXECUTION //
            if vm.containsQuickActionButtontwo {
                Button(
                    action:{
                        vm.handleQuickActionButtontwoPressed()
                    },
                    label: {
                        HStack {
                            Image(systemName: "stop.circle.fill")
                                .font(.largeTitle)
                        }
                    })
                .buttonStyle(.plain)
            }
            
            NavigationLink(destination: ActionStateDetailedView(vm: ActionStateDetailedViewModel(actionState: vm.actionState, actionStateListVM: vm.actionStateListVM))) {
                Text(vm.actionState.title)
            }
        }

    }
}




//struct ActionStateRowView_Previews: PreviewProvider {
//    static var previews: some View {
//        ActionStateRowView()
//    }
//}
